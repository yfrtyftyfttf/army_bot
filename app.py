from flask import Flask, request, jsonify
from flask_cors import CORS
import telebot
from telebot import types
import uuid
import os
from threading import Thread

# ====== الإعدادات ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")
PRICE_PER_1000 = 3.0

if BOT_TOKEN is None or ADMIN_ID is None:
    print("❌ BOT_TOKEN أو ADMIN_ID غير موجودين في Render Environment")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)
CORS(app)

# ====== قواعد بيانات مؤقتة ======
users = {}
orders = {}

def calc_price(qty):
    return round((qty / 1000) * PRICE_PER_1000, 2)

@app.route("/api/register", methods=["POST"])
def register():
    uid = str(uuid.uuid4())[:8]
    users[uid] = {"balance": 0.0, "orders": []}
    return jsonify({"user_id": uid})

@app.route("/api/balance/<uid>")
def balance(uid):
    return jsonify(users.get(uid, {}))

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
        f"💰 طلب شحن\n👤 المستخدم: {uid}\n💵 المبلغ: ${amount}",
        reply_markup=markup
    )
    return jsonify({"status": "sent"})

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
        f"🚀 طلب جديد\n🆔 {order_id}\n📱 {platform}\n🔢 {qty}\n🔗 {link}",
        reply_markup=markup
    )

    return jsonify({"order_id": order_id})

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    data = call.data.split("_")

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

    if data[0] == "ord":
        order_id = data[2]
        if data[1] == "proc":
            orders[order_id]["status"] = "processing"
        elif data[1] == "done":
            orders[order_id]["status"] = "completed"

if __name__ == "__main__":
    Thread(target=bot.infinity_polling, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
