import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# السماح لجميع النطاقات بالوصول لمنع مشكلة فشل الاتصال
CORS(app, resources={r"/*": {"origins": "*"}}) 

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/')
def home():
    return "Server is Running!"

@app.route('/send_order', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.json
        # استخراج البيانات مع قيم افتراضية لمنع توقف الكود
        o_type = data.get('type', 'Unknown')
        u_name = data.get('user_name', 'Customer')
        acc_code = data.get('acc_code', '000000')
        details = data.get('details', {})

        msg = f"🔔 طلب جديد: {o_type}\n👤 المستخدم: {u_name}\n🆔 الكود: {acc_code}\n"
        for k, v in details.items():
            msg += f"🔹 {k}: {v}\n"

        # إرسال للتليجرام
        res = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": msg,
            "reply_markup": {"inline_keyboard": [[{"text": "✅ تنفيذ", "callback_data": "done"}]]}
        })
        
        return jsonify({"status": "success", "tele_res": res.status_code}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    # نظام البحث عن كود الحساب
    if "message" in update and update["message"].get("text", "").isdigit():
        code = int(update["message"]["text"])
        if len(str(code)) == 6:
            users = db.collection('users').where('accountCode', '==', code).get()
            for u in users:
                user = u.to_dict()
                msg = f"👤 مستخدم: {user['name']}\n💰 الرصيد: {user['balance']}$\n🆔 الكود: {user['accountCode']}"
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                    "chat_id": CHAT_ID, "text": msg,
                    "reply_markup": {"inline_keyboard": [[{"text": "➕ إضافة 5$", "callback_data": f"add_{user['uid']}_5"}]]}
                })
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Render يحتاج تشغيل على المنفذ 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
