from flask import Flask, request
import telebot
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

webhook_set = False  # مهم جدًا

# ===== Telegram =====
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(msg.chat.id, "✅ البوت شغال ومربوط بالسيرفر")

# ===== Web =====
@app.route("/")
def home():
    return "Server is running ✅"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(
        request.get_data(as_text=True)
    )
    bot.process_new_updates([update])
    return "OK", 200

# ===== Set webhook safely =====
@app.before_request
def set_webhook_once():
    global webhook_set
    if not webhook_set:
        bot.remove_webhook()
        bot.set_webhook(
            url=f"https://army-bot-3y9o.onrender.com/{BOT_TOKEN}"
        )
        webhook_set = True

# ===== Run =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
