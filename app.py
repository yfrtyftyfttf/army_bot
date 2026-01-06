from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import uuid
import os
from threading import Thread

# ====== الإعدادات من Environment ======
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")
PRICE_PER_1000 = 3.0

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app, origins=["https://yfrtyftyfttf.github.io"])

# ====== قواعد بيانات مؤقتة ======
users = {}
orders = {}

# ====== دوال ======
def calc_price(qty):
    return round((qty / 1000) * PRICE_PER_1000, 2)

# ====== تسجيل مستخدم ======
@app.route("/api/register", methods=["POST"])
def register():
    uid = str(uuid.uuid4())[:8]
    users[uid] = {"balance": 0.0, "orders": []}
    return jsonify({"user_id": uid})

# ====== الرصيد ======
@app.route("/api/balance/<uid>")
def balance(uid):
    if uid not in users:
        return jsonify({"error": "user not found"}), 404
    return jsonify(users[uid])

# ====== شحن ======
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
        f"💰 طلب شحن\n👤 {uid}\n💵 ${amount}",
        reply_markup=markup
    )

    return jsonify({"status": "sent"})

# ====== طلب ======
@app.route("/api/order", methods=["POST"])
def order():
    data = request.json
    uid = data["user_id"]

    if uid not in users:
        return jsonify({"error": "user not found"}), 404

    qty = int(data["qty"])
    cost = calc_price(qty)

    if users[uid]["balance"] < cost:
        return jsonify({"error": "رصيد غير كافي"}), 400

    users[uid]["balance"] -= cost
    oid = str(uuid.uuid4())[:8]

    orders[oid] = {
        "status": "pending",
        "user": uid
    }

    users[uid]["orders"].append(oid)

    bot.send_message(ADMIN_ID, f"🚀 طلب جديد\nID: {oid}")

    return jsonify({"order_id": oid})

# ====== بوت ======
@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    d = call.data.split("_")

    if d[0] == "dep":
        uid = d[2]
        if d[1] == "ok":
            amount = float(d[3])
            users[uid]["balance"] += amount
            bot.edit_message_text("✅ تم الشحن", call.message.chat.id, call.message.message_id)
        else:
            bot.edit_message_text("❌ مرفوض", call.message.chat.id, call.message.message_id)

# ====== تشغيل البوت ======
Thread(target=bot.infinity_polling, daemon=True).start()
