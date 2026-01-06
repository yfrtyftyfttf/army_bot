from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import uuid

# ====== الإعدادات ======
TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID = "6695916631"
PRICE_PER_1000 = 3.0

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app)

# ====== قواعد بيانات بسيطة (لاحقًا MySQL) ======
users = {}
orders = {}

# ====== دوال مساعدة ======
def calc_price(qty):
    return round((qty / 1000) * PRICE_PER_1000, 2)

# ====== تسجيل مستخدم ======
@app.route("/api/register", methods=["POST"])
def register():
    uid = str(uuid.uuid4())[:8]
    users[uid] = {
        "balance": 0.0,
        "orders": []
    }
    return jsonify({"user_id": uid})

# ====== جلب الرصيد ======
@app.route("/api/balance/<uid>", methods=["GET"])
def balance(uid):
    return jsonify(users.get(uid, {}))

# ====== طلب شحن ======
@app.route("/api/deposit", methods=["POST"])
def deposit():
    data = request.json
    uid = data["user_id"]
    amount = float(data["amount"])

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ شحن", callback_data=f"dep_ok_{uid}_{amount}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"dep_no_{uid}")
    )

    bot.send_message(
        ADMIN_ID,
        f"💰 طلب شحن رصيد\n"
        f"👤 المستخدم: {uid}\n"
        f"💵 المبلغ: ${amount}",
        reply_markup=markup
    )

    return jsonify({"status": "sent"})

# ====== إنشاء طلب رشق ======
@app.route("/api/order", methods=["POST"])
def order():
    data = request.json
    uid = data["user_id"]
    platform = data["platform"]
    qty = int(data["qty"])
    link = data["link"]

    cost = calc_price(qty)

    if users[uid]["balance"] < cost:
        return jsonify({"error": "رصيد غير كافي"}), 400

    users[uid]["balance"] -= cost

    order_id = str(uuid.uuid4())[:8]
    orders[order_id] = {
        "user": uid,
        "platform": platform,
        "qty": qty,
        "link": link,
        "cost": cost,
        "status": "pending"
    }

    users[uid]["orders"].append(order_id)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔄 قيد التنفيذ", callback_data=f"ord_proc_{order_id}"),
        types.InlineKeyboardButton("✅ مكتمل", callback_data=f"ord_done_{order_id}")
    )

    bot.send_message(
        ADMIN_ID,
        f"🚀 طلب رشق جديد\n"
        f"🆔 ID: {order_id}\n"
        f"📱 المنصة: {platform}\n"
        f"🔢 الكمية: {qty}\n"
        f"🔗 الرابط: {link}\n"
        f"💵 السعر: ${cost}",
        reply_markup=markup
    )

    return jsonify({"order_id": order_id, "cost": cost})

# ====== مراقبة الطلب ======
@app.route("/api/order/<order_id>", methods=["GET"])
def track(order_id):
    return jsonify(orders.get(order_id, {}))

# ====== أوامر البوت ======
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    data = call.data.split("_")

    # شحن رصيد
    if data[0] == "dep":
        uid = data[2]
        if data[1] == "ok":
            amount = float(data[3])
            users[uid]["balance"] += amount
            bot.edit_message_text(
                f"✅ تم شحن ${amount} للمستخدم {uid}",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            bot.edit_message_text("❌ تم رفض الشحن",
                call.message.chat.id,
                call.message.message_id
            )

    # إدارة الطلب
    if data[0] == "ord":
        order_id = data[2]
        if data[1] == "proc":
            orders[order_id]["status"] = "processing"
            bot.answer_callback_query(call.id, "تم تحويل الطلب قيد التنفيذ")
        elif data[1] == "done":
            orders[order_id]["status"] = "completed"
            bot.edit_message_text(
                f"✅ الطلب {order_id} مكتمل",
                call.message.chat.id,
                call.message.message_id
            )

# ====== تشغيل ======
if __name__ == "__main__":
    from threading import Thread
    Thread(target=bot.infinity_polling).start()
    app.run(host="0.0.0.0", port=5000)
