import telebot
import requests
import os

# --- [1] إعدادات الهوية ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
ADMIN_ID = 6695916631 

bot = telebot.TeleBot(BOT_TOKEN)

# --- [2] وظيفة ذكية لقراءة البروكسيات من الملف ---
def get_proxies_from_file():
    if os.path.exists('m2.txt'):
        with open('m2.txt', 'r') as f:
            # يقرأ كل سطر ويضعه في قائمة تلقائياً
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def check_insta_and_email(username):
    proxies_list = get_proxies_from_file()
    if not proxies_list:
        return "⚠️ لا يوجد بروكسيات في ملف m2.txt"
    
    # استخدام أول بروكسي كمثال
    proxy = proxies_list[0]
    p = proxy.split(':')
    p_dict = {
        "http": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}",
        "https": f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
    }
    
    try:
        url = f"https://www.instagram.com/{username}/"
        res = requests.get(url, proxies=p_dict, timeout=7)
        if res.status_code == 404:
            return f"🎯 @{username} متاح في انستا! \n📧 افحص الإيميل: {username}@hotmail.com"
        return f"❌ @{username} غير متاح."
    except:
        return "⚠️ البروكسي لا يعمل، جرب فحص مرة أخرى."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 الأداة جاهزة! أرسل اليوزر للصيد:")

@bot.message_handler(func=lambda m: True)
def handle(message):
    res = check_insta_and_email(message.text)
    bot.send_message(ADMIN_ID, res)

bot.infinity_polling()
