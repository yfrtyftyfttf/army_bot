import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# هذا السطر هو مفتاح الحل لربط الموقع بالسيرفر
CORS(app, resources={r"/*": {"origins": "*"}})

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/send_order', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    try:
        data = request.json
        u_uid = data.get('user_uid')
        u_name = data.get('user_name')
        amt = data.get('details', {}).get('المبلغ', 0)
        
        msg = f"🔔 طلب شحن جديد\n👤 الاسم: {u_name}\n💰 المبلغ: {amt}$\n🆔 كود: {data.get('acc_code')}"
        
        # زر الموافقة يحتوي على الـ UID والمبلغ لتنفيذ الشحن فوراً
        kb = [[{"text": "✅ موافقة وإضافة الرصيد", "callback_data": f"confirm_{u_uid}_{amt}"}]]
        
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "reply_markup": {"inline_keyboard": kb}})
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    if "callback_query" in update:
        call = update["callback_query"]
        data = call["data"]
        
        if data.startswith("confirm_"):
            # استخراج البيانات: confirm_USERID_AMOUNT
            parts = data.split("_")
            uid = parts[1]
            amount = float(parts[2])
            
            # تحديث Firebase فعلياً
            user_ref = db.collection('users').document(uid)
            user_ref.update({'balance': firestore.Increment(amount)})
            
            # إشعار الأدمن بنجاح العملية
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", 
                          json={"chat_id": CHAT_ID, "message_id": call["message"]["message_id"], 
                                "text": call["message"]["text"] + f"\n\n✅ تم شحن {amount}$ للحساب بنجاح!"})
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
