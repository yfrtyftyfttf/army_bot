import telebot
import os

# --- إعدادات البوت ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
ADMIN_ID = 6695916631

bot = telebot.TeleBot(BOT_TOKEN)

# وظيفة قراءة البروكسيات من ملف m2.txt
def get_proxies_from_file():
    if os.path.exists('m2.txt'):
        with open('m2.txt', 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    proxies = get_proxies_from_file()
    count = len(proxies)
    bot.reply_to(message, f"أهلاً بك! تم تحميل {count} بروكسي من ملف m2.txt بنجاح.")

print("البوت بدأ العمل...")
bot.infinity_polling()
