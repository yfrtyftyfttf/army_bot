from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import os

# --- بياناتك ---
TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID = "6695916631"
# --------------

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app) # تم إصلاح خطأ مكتبة CORS هنا

# مخزن مؤقت للطلبات (سيختفي عند إعادة تشغيل السيرفر)
orders = {}

@app.route('/')
def home():
    return "نظام محمد يعمل بنجاح!"

# استقبال الطلب من الموقع
@app.route('/api/order', methods=['POST']) # تم إصلاح الخطأ من list إلى methods هنا
def create_order():
    data = request.json
    order_id = data.get('orderId')
    
    # حفظ حالة الطلب
    orders[str(order_id)] = {"status": "قيد التنفيذ"}

    # إرسال زر التحكم للمدير في تليجرام
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("✅ تم إكمال الطلب", callback_data=f"done_{order_id}")
    markup.add(btn)

    msg = (f"🚀 طلب جديد #{order_id}\n"
           f"🛠 الخدمة: {data.get('service')}\n"
           f"🔗 الرابط: {data.get('link')}\n"
           f"🔢 الكمية: {data.get('qty')}\n"
           f"💵 التكلفة: ${data.get('cost')}")
    
    bot.send_message(ADMIN_ID, msg, reply_markup=markup)
    return jsonify({"success": True})

# فحص الحالة للموقع
@app.route('/api/status/<order_id>', methods=['GET'])
def get_status(order_id):
    order = orders.get(str(order_id))
    return jsonify({"status": order['status'] if order else "غير موجود"})

# زر "تم الإكمال"
@bot.callback_query_handler(func=lambda call: call.data.startswith('done_'))
def handle_done(call):
    order_id = call.data.split('_')[1]
    if order_id in orders:
        orders[order_id]['status'] = "تم المكتمل"
        bot.edit_message_text(f"✅ الطلب #{order_id} تم تنفيذه!", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id, "تم تحديث حالة الطلب للمستخدم")

if __name__ == "__main__":
    from threading import Thread
    def run_bot():
        bot.polling(none_stop=True)
    
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
