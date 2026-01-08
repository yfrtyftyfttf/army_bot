import os
import random
import requests
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# تهيئة Firebase مع التأكد من المسار الصحيح
try:
    if not firebase_admin._apps:
        # استخدام المسار المطلق للملف لضمان العثور عليه
        base_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_path, "serviceAccountKey.json")
        cred = credentials.Certificate(json_path)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ تم الربط مع Firebase بنجاح")
except Exception as e:
    print(f"❌ خطأ في تهيئة Firebase: {str(e)}")

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

@app.route('/')
def home():
    return "سيرفر الجيش يعمل!"

@app.route('/send_order', methods=['POST'])
def send_order():
    try:
        data = request.json
        u_uid = data.get('user_uid')
        u_name = data.get('user_name', 'عميل')
        o_type = data.get('type')
        details = data.get('details', {})
        o_id = f"{random.randint(1000, 9999)}"

        text = f"📦 طلب #{o_id} جديد\n👤 العميل: {u_name}\n🆔 UID: {u_uid}\n"
        text += "------------------------\n"
        for key, value in details.items():
            text += f"🔹 {key}: {value}\n"

        if o_type == 'شحن رصيد':
            amt = details.get('المبلغ', '0')
            buttons = [[
                {"text": "✅ قبول وشحن", "callback_data": f"add_{u_uid}_{amt}_{o_id}"},
                {"text": "❌ رفض", "callback_data": f"rej_{o_id}"}
            ]]
        else:
            prc = str(details.get('السعر', '0')).replace('$', '')
            buttons = [
                [{"text": "✅ تم التنفيذ", "callback_data": f"done_{o_id}"}],
                [{"text": f"❌ رفض وإرجاع {prc}$", "callback_data": f"ref_{u_uid}_{prc}_{o_id}"}]
            ]

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID, "text": text, "reply_markup": {"inline_keyboard": buttons}
        })
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    if "callback_query" in update:
        query = update["callback_query"]
        callback_data = query["data"]
        msg_id = query["message"]["message_id"]
        chat_id = query["message"]["chat"]["id"]
        
        parts = callback_data.split('_')
        action = parts[0]
        
        try:
            if action == "add": 
                uid, amt, oid = parts[1], float(parts[2]), parts[3]
                db.collection('users').document(uid).update({'balance': firestore.Increment(amt)})
                res_txt = f"✅ تم شحن {amt}$ للطلب #{oid}"
            elif action == "ref": 
                uid, prc, oid = parts[1], float(parts[2]), parts[3]
                db.collection('users').document(uid).update({'balance': firestore.Increment(prc)})
                res_txt = f"💰 تم رفض #{oid} وإرجاع {prc}$"
            elif action == "done":
                res_txt = f"🎉 تم تنفيذ الطلب #{parts[1]}"
            elif action == "rej":
                res_txt = f"❌ تم رفض الطلب #{parts[1]}"

            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText", json={
                "chat_id": chat_id, "message_id": msg_id, "text": f"{query['message']['text']}\n\n⚙️ النتيجة: {res_txt}"
            })
        except Exception as e:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                "chat_id": chat_id, "text": f"⚠️ خطأ Firebase: {str(e)}"
            })
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
