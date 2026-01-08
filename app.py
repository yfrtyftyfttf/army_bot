import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# تفعيل CORS لجميع النطاقات لضمان اتصال الموقع بالسيرفر
CORS(app, resources={r"/*": {"origins": "*"}})

# تهيئة Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/')
def health_check():
    return "Server is Live!", 200

# المسار الخاص باستلام الطلبات من الموقع
@app.route('/send_order', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.json
        print(f"Received data: {data}") # للتأكد من وصول البيانات في الـ Logs

        u_name = data.get('user_name', 'Customer')
        o_type = data.get('type', 'Order')
        acc_code = data.get('acc_code', '------')
        details = data.get('details', {})

        msg = f"🔔 طلب جديد: {o_type}\n👤 العميل: {u_name}\n🆔 كود الحساب: {acc_code}\n"
        for k, v in details.items():
            msg += f"🔹 {k}: {v}\n"

        # إرسال للتليجرام مع زر التفاعل
        kb = [[{"text": "✅ تنفيذ / شحن", "callback_data": f"approve_{data.get('user_uid')}"}]]
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "reply_markup": {"inline_keyboard": kb}})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# المسار الخاص بـ Webhook التليجرام (البحث عن الكود)
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    if "message" in update:
        text = update["message"].get("text", "")
        chat_id = update["message"]["chat"]["id"]
        
        # إذا أرسل الأدمن كود من 6 أرقام، ابحث عنه
        if text.isdigit() and len(text) == 6:
            users = db.collection('users').where('accountCode', '==', int(text)).get()
            found = False
            for u in users:
                user = u.to_dict()
                found = True
                msg = f"🔍 تم العثور على الحساب:\n👤 الاسم: {user['name']}\n💰 الرصيد: {user['balance']}$\n🆔 الكود: {user['accountCode']}"
                kb = [[{"text": "➕ إضافة رصيد", "callback_data": f"recharge_{user['uid']}"}]]
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              json={"chat_id": chat_id, "text": msg, "reply_markup": {"inline_keyboard": kb}})
            if not found:
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              json={"chat_id": chat_id, "text": "❌ لم يتم العثور على حساب بهذا الكود."})
    
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Render يستخدم المنفذ 10000
    app.run(host='0.0.0.0', port=10000)
