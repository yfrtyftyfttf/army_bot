import os
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# السماح الشامل لكل النطاقات لمنع فشل الاتصال من المتصفح
CORS(app, resources={r"/*": {"origins": "*"}})

# تهيئة Firebase (تأكد من وجود ملف الـ JSON في نفس المجلد)
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/')
def home():
    # هذا المسار يمنع ظهور خطأ 404 عند فتح رابط السيرفر مباشرة
    return "Server is Running Successfully!", 200

@app.route('/send_order', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.json
        u_uid = data.get('user_uid')
        u_name = data.get('user_name', 'Customer')
        acc_code = data.get('acc_code', '000000')
        o_type = data.get('type', 'Order')
        details = data.get('details', {})

        # تجهيز الرسالة للتليجرام
        msg = f"🔔 طلب جديد: {o_type}\n👤 العميل: {u_name}\n🆔 الكود: {acc_code}\n"
        for k, v in details.items():
            msg += f"🔹 {k}: {v}\n"

        # إذا كان الطلب "شحن رصيد"، نضع زر "موافقة" يحتوي على المبلغ والـ UID
        reply_markup = None
        if o_type == 'شحن رصيد':
            amount = details.get('المبلغ', 0)
            reply_markup = {
                "inline_keyboard": [[
                    {"text": "✅ موافقة وشحن الرصيد", "callback_data": f"confirm_{u_uid}_{amount}"}
                ]]
            }

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "reply_markup": reply_markup})
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    
    # معالجة الضغط على زر الموافقة
    if "callback_query" in update:
        call = update["callback_query"]
        data = call["data"]
        
        if data.startswith("confirm_"):
            parts = data.split("_")
            u_uid = parts[1]
            amount = float(parts[2])
            
            # تحديث الرصيد في Firebase
            user_ref = db.collection('users').document(u_uid)
            user_ref.update({'balance': firestore.Increment(amount)})
            
            # تحديث رسالة التليجرام لتأكيد العملية
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", 
                          json={
                              "chat_id": CHAT_ID, 
                              "message_id": call["message"]["message_id"], 
                              "text": call["message"]["text"] + f"\n\n✅ تم شحن {amount}$ بنجاح!"
                          })
            
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # المنفذ 10000 هو الافتراضي لـ Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
