import telebot
import threading
import time
import random
import os

# --- ⚙️ إعدادات البوت ---
BOT_TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID =  6695916631   # الآيدي الخاص بك
# -----------------------

bot = telebot.TeleBot(BOT_TOKEN)
is_running = False

# وظيفة قراءة البروكسيات من ملف m2.txt
def get_proxies_from_file():
    if os.path.exists('m.txt'):
        with open('m.txt', 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def factory_engine():
    global is_running
    proxies = get_proxies_from_file()
    
    if not proxies:
        bot.send_message(ADMIN_ID, "❌ خطأ: لم أجد بروكسيات في ملف m2.txt!")
        is_running = False
        return

    bot.send_message(ADMIN_ID, f"🚀 بدأ الإنتاج! تم تحميل {len(proxies)} بروكسي.")
    
    while is_running:
        p = random.choice(proxies).split(':')
        user_fake = f"mo_{random.randint(100, 999)}_sec"
        
        # رسالة تقرير لك على تليجرام
        log_txt = f"🛡️ **تقرير المصنع:**\n👤 الحساب: `{user_fake}`\n🌐 البروكسي: `{p[0]}`\n✅ الحالة: مستمر.."
        bot.send_message(ADMIN_ID, log_txt, parse_mode="Markdown")
        
        time.sleep(20) # تأخير بسيط لضمان استقرار السيرفر

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if str(message.from_user.id) == str(ADMIN_ID):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🚀 تشغيل المصنع", "🛑 إيقاف المصنع")
        bot.send_photo(message.chat.id, "https://i.ibb.co/m5YfM5y/image.png", 
                       caption="لوحة تحكم MOHAMED SECURITY 🛡️\n\nالسيرفر جاهز وقارئ لملف m2.txt", 
                       reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_control(message):
    global is_running
    if str(message.from_user.id) == str(ADMIN_ID):
        if message.text == "🚀 تشغيل المصنع":
            if not is_running:
                is_running = True
                threading.Thread(target=factory_engine, daemon=True).start()
                bot.send_message(ADMIN_ID, "⚙️ جاري تشغيل المحرك...")
            else:
                bot.send_message(ADMIN_ID, "⚠️ المصنع يعمل بالفعل.")
        elif message.text == "🛑 إيقاف المصنع":
            is_running = False
            bot.send_message(ADMIN_ID, "🛑 تم إيقاف الإنتاج.")

if __name__ == "__main__":
    # تشغيل البوت باستمرار
    bot.infinity_polling()
