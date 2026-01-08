import os
import random
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. تهيئة Firebase باستخدام الملف الذي رفعته
# تأكد أن اسم الملف في GitHub هو serviceAccountKey.json بالضبط
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. إعدادات التليجرام الخاصة بك
BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/')
def home():
    return "سيرفر الجيش يعمل بنجاح!"

# استقبال الطلبات من الموقع
@app.route('/send_order', methods=['POST'])
def send_order():
    try:
        data = request.json
        order_type = data.get('type')
        details = data.get('details')
        user_uid = data.get('user_uid')
        user_name = data.get('user_name', 'عميل')
        order_id = f"{random.randint(1000, 9999)}"

        text = f"📦 طلب #{order_id} جديد\n👤 العميل: {user_name}\n🆔 UID: {user_uid}\n"
        text += "------------------------\n"
        for key, value in details.items():
            text += f"🔹 {key}: {value}\n"

        # إعداد الأزرار (أصلحت لك الروابط لتكون متوافقة مع الـ Webhook)
        if order_type == 'شحن رصيد':
            amount = details.get('المبلغ', '0')
            buttons = [[
                {"text": "✅ قبول وشحن", "callback_data": f"add_{user_uid}_{amount}_{order_id}"},
                {"text": "❌ رفض", "callback_data": f"rej_{order_id}"}
            ]]
        else:
            price = details.get('السعر', '0').replace('$', '')
            buttons = [
                [{"text": "✅ تم التنفيذ", "callback_data": f"done_{order_id}"}],
                [{"text": f"❌ رفض وإرجاع {price}$", "callback_data": f"ref_{user_uid}_{price}_{order_id}"}]
            ]

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": text,
            "reply_markup": {"inline_keyboard": buttons}
        })
        return jsonify({"status": "success", "order_id": order_id}), 200
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

# معالجة ضغطات الأزرار من التليجرام (Webhook)
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    if "callback_query" in update:
        query = update["callback_query"]
        data = query["data"].split('_')
        action = data[0]
        msg_id = query["message"]["message_id"]
        
        log_msg = ""
        try:
            if action == "add":
                uid, amt, oid = data[1], float(data[2]), data[3]
                db.collection('users').doc(uid).update({'balance': firestore.Increment(amt)})
                log_msg = f"✅ تم شحن {amt}$ للطلب #{oid}"
            elif action == "ref":
                uid, prc, oid = data[1], float(data[2]), data[3]
                db.collection('users').doc(uid).update({'balance': firestore.Increment(prc)})
                log_msg = f"💰 تم رفض #{oid} وإرجاع {prc}$"
            elif action == "done":
                log_msg = f"🎉 تم تنفيذ الطلب #{data[1]}"
            elif action == "rej":
                log_msg = f"❌ تم رفض الطلب #{data[1]}"

            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", json={
                "chat_id": CHAT_ID,
                "message_id": msg_id,
                "text": f"{query['message']['text']}\n\n⚙️ الإجراء: {log_msg}"
            })
        except Exception as e:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                "chat_id": CHAT_ID, "text": f"❌ خطأ في النظام: {str(e)}"
            })
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
