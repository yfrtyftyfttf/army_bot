import os
import random
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# تهيئة Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

BOT_TOKEN = "7465926974:AAHzPv067I1ser4kExbRt5Hzj9R3Ma5Xjik"
CHAT_ID = "6695916631"

# --- دالة إرسال إشعار للمستخدم عبر البوت ---
def notify_user(uid, message):
    # ملاحظة: لكي يعمل هذا، يجب أن يكون المستخدم قد بدأ محادثة مع البوت سابقاً
    # سنقوم بالبحث عن الـ Chat ID الخاص به في قاعدة البيانات (اختياري)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # هنا نفترض أن UID المستخدم هو نفسه Chat ID تليجرام الخاص به لسهولة الربط
    requests.post(url, json={"chat_id": uid, "text": message})

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.json
    
    # التحقق من وجود ضغطة زر (Callback Query)
    if "callback_query" in update:
        callback_data = update["callback_query"]["data"]
        user_uid_from_tg = update["callback_query"]["from"]["id"] # لمعرفة من ضغط الزر (أنت الأدمن)
        
        # تفكيك البيانات من الزر: (العملية_UID_المبلغ_رقمالطلب)
        parts = callback_data.split('_')
        action = parts[0]
        
        if action == "add": # قبول شحن رصيد
            target_uid = parts[1]
            amount = float(parts[2])
            order_id = parts[3]
            
            # تحديث الرصيد في Firestore
            user_ref = db.collection('users').doc(target_uid)
            user_ref.update({'balance': firestore.Increment(amount)})
            
            response_text = f"✅ تم شحن {amount}$ للطلب #{order_id} بنجاح!"
            
        elif action == "ref": # رفض وإرجاع مبلغ الرشق
            target_uid = parts[1]
            amount = float(parts[2])
            order_id = parts[3]
            
            # إعادة المال للمحفظة
            user_ref = db.collection('users').doc(target_uid)
            user_ref.update({'balance': firestore.Increment(amount)})
            
            response_text = f"💰 تم رفض الطلب #{order_id} وإعادة {amount}$ للعميل."

        elif action == "done":
            order_id = parts[1]
            response_text = f"🎉 تم تأكيد تنفيذ الطلب #{order_id}."

        # إرسال إشعار لك (الأدمن) بأن العملية تمت
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": response_text})
        
    return jsonify({"status": "ok"}), 200

@app.route('/send_order', methods=['POST'])
def send_order():
    try:
        data = request.json
        order_type = data.get('type')
        details = data.get('details')
        user_uid = data.get('user_uid')
        user_name = data.get('user_name', 'عميل')
        order_id = f"{random.randint(1000, 9999)}"

        text = f"📦 طلب جديد #{order_id}\n👤 العميل: {user_name}\n"
        for key, value in details.items(): text += f"🔹 {key}: {value}\n"

        # بناء الأزرار بنفس التنسيق المذكور في المعالج
        if order_type == 'شحن رصيد':
            amount = details.get('المبلغ', '0')
            buttons = [[{"text": "✅ قبول الشحن", "callback_data": f"add_{user_uid}_{amount}_{order_id}"}]]
        else:
            price = details.get('السعر', '0').replace('$', '')
            buttons = [[
                {"text": "✅ تم", "callback_data": f"done_{order_id}"},
                {"text": "❌ رفض وإرجاع", "callback_data": f"ref_{user_uid}_{price}_{order_id}"}
            ]]

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": text, "reply_markup": {"inline_keyboard": buttons}})
        
        return jsonify({"status": "success", "order_id": order_id}), 200
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
