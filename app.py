from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import os

# إعدادات البوت
TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID = "6695916631"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app)

# مخزن مؤقت للطلبات
orders = {}

@app.route('/')
def home():
    return "Server is Running!"

# استقبال الطلب من الموقع
@app.route('/api/order', list=['POST'])
def create_order():
    data = request.json
    order_id = data.get('orderId')
    link = data.get('link')
    qty = data.get('qty')
    service = data.get('service')
    cost = data.get('cost')

    # حفظ الطلب
    orders[str(order_id)] = {"status": "قيد التنفيذ", "details": data}

    # إرسال للمدير في تليجرام
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ تم إكمال الطلب", callback_data=f"done_{order_id}")
    markup.add(btn)

    msg = f"🚀 طلب جديد #{order_id}\n🛠 الخدمة: {service}\n🔗 الرابط: {link}\n🔢 الكمية: {qty}\n💵 التكلفة: ${cost}"
    bot.send_message(ADMIN_ID, msg, reply_markup=markup)
    
    return jsonify({"success": True})

# فحص حالة الطلب من الموقع
@app.route('/api/status/<order_id>')
def get_status(order_id):
    order = orders.get(str(order_id))
    return jsonify({"status": order['status'] if order else "غير موجود"})

# التعامل مع زر "تم الإكمال"
@bot.callback_query_handler(func=lambda call: call.data.startswith('done_'))
def handle_done(call):
    order_id = call.data.split('_')[1]
    if order_id in orders:
        orders[order_id]['status'] = "تم المكتمل"
        bot.edit_message_text(f"✅ الطلب #{order_id} اكتمل بنجاح!", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "تم تحديث الحالة للمستخدم!")

# تشغيل البوت والسيرفر
if __name__ == "__main__":
    from threading import Thread
    def run_bot():
        bot.polling(none_stop=True)
    
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
