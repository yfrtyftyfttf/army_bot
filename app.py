import telebot
import threading
import time
import random

# --- ⚙️ إعدادات التحكم ---
BOT_TOKEN = "6785445743:AAFquuyfY2IIjgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID =  "6695916631"
# -----------------------

# --- 🟢 قائمة البروكسيات ---
proxies_data = """
82.24.249.101:5938:njhuvsdz:wp92l0dkdkoc 
82.29.244.57:5880:njhuvsdz:wp92l0dkdkoc 
198.89.123.107:6649:njhuvsdz:wp92l0dkdkoc 
206.206.71.75:5715:njhuvsdz:wp92l0dkdkoc 
23.27.210.135:6505:njhuvsdz:wp92l0dkdkoc 
64.137.49.9:6550:njhuvsdz:wp92l0dkdkoc 
66.63.180.174:5698:njhuvsdz:wp92l0dkdkoc 
149.57.17.176:5644:njhuvsdz:wp92l0dkdkoc 
154.6.59.162:6630:njhuvsdz:wp92l0dkdkoc 
91.211.87.224:7214:njhuvsdz:wp92l0dkdkoc 
199.180.8.177:5888:njhuvsdz:wp92l0dkdkoc 
82.24.247.128:6962:njhuvsdz:wp92l0dkdkoc 
198.105.119.196:5445:njhuvsdz:wp92l0dkdkoc 
82.21.244.100:5423:njhuvsdz:wp92l0dkdkoc 
82.25.213.249:5601:njhuvsdz:wp92l0dkdkoc 
31.59.27.107:6684:njhuvsdz:wp92l0dkdkoc 
45.43.87.128:7877:njhuvsdz:wp92l0dkdkoc 
64.137.89.162:6235:njhuvsdz:wp92l0dkdkoc 
142.147.245.203:5894:njhuvsdz:wp92l0dkdkoc 
23.229.125.169:5438:njhuvsdz:wp92l0dkdkoc 
31.223.189.234:6500:njhuvsdz:wp92l0dkdkoc 
45.41.171.41:6077:njhuvsdz:wp92l0dkdkoc 
205.164.57.143:5718:njhuvsdz:wp92l0dkdkoc 
82.23.222.10:6316:njhuvsdz:wp92l0dkdkoc 
209.242.203.117:6832:njhuvsdz:wp92l0dkdkoc 
64.137.8.175:6857:njhuvsdz:wp92l0dkdkoc 
23.27.138.82:6183:njhuvsdz:wp92l0dkdkoc 
142.147.244.113:6357:njhuvsdz:wp92l0dkdkoc 
82.23.222.38:6344:njhuvsdz:wp92l0dkdkoc 
23.27.208.117:5827:njhuvsdz:wp92l0dkdkoc 
31.59.33.141:6717:njhuvsdz:wp92l0dkdkoc 
142.202.254.57:6035:njhuvsdz:wp92l0dkdkoc 
82.22.235.92:6898:njhuvsdz:wp92l0dkdkoc 
195.40.187.2:5184:njhuvsdz:wp92l0dkdkoc 
66.63.180.153:5677:njhuvsdz:wp92l0dkdkoc 
82.29.249.54:7891:njhuvsdz:wp92l0dkdkoc 
108.165.227.16:5257:njhuvsdz:wp92l0dkdkoc 
82.24.217.12:5342:njhuvsdz:wp92l0dkdkoc 
45.131.92.195:6806:njhuvsdz:wp92l0dkdkoc 
104.245.244.5:6445:njhuvsdz:wp92l0dkdkoc 
145.223.47.135:6717:njhuvsdz:wp92l0dkdkoc 
64.137.99.193:5826:njhuvsdz:wp92l0dkdkoc 
204.217.161.171:6743:njhuvsdz:wp92l0dkdkoc 
107.181.148.69:5929:njhuvsdz:wp92l0dkdkoc 
173.211.30.43:6477:njhuvsdz:wp92l0dkdkoc 
181.214.13.96:5937:njhuvsdz:wp92l0dkdkoc 
104.252.41.95:7032:njhuvsdz:wp92l0dkdkoc 
45.41.171.35:6071:njhuvsdz:wp92l0dkdkoc 
46.203.154.160:5603:njhuvsdz:wp92l0dkdkoc 
82.23.204.254:7086:njhuvsdz:wp92l0dkdkoc
"""
# --------------------------

bot = telebot.TeleBot(BOT_TOKEN)
MY_PROXIES = [line.strip() for line in proxies_data.strip().split('\n') if line.strip()]
is_running = False

def factory_engine():
    global is_running
    bot.send_message(ADMIN_ID, "🚀 تم تشغيل المصنع بنجاح.. جاري بدء الإنتاج!")
    
    while is_running:
        # هنا تضع كود إنشاء الحسابات الخاص بك
        # مثال على إرسال تقرير لكل عملية:
        p = random.choice(MY_PROXIES).split(':') if MY_PROXIES else ["127.0.0.1"]
        user_fake = f"mo_{random.randint(100, 999)}_sec"
        
        log_msg = f"✅ محاولة جديدة:\n👤 User: {user_fake}\n🌐 Proxy: {p[0]}\n⚙️ Status: Running..."
        bot.send_message(ADMIN_ID, log_msg)
        
        time.sleep(10) # الوقت بين كل عملية

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id == ADMIN_ID:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("🚀 تشغيل المصنع")
        btn2 = telebot.types.KeyboardButton("🛑 إيقاف المصنع")
        markup.add(btn1, btn2)
        bot.reply_to(message, "مرحباً بك في لوحة تحكم MOHAMED SECURITY 🛡️", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def control_factory(message):
    global is_running
    if message.from_user.id == ADMIN_ID:
        if message.text == "🚀 تشغيل المصنع":
            if not is_running:
                is_running = True
                threading.Thread(target=factory_engine, daemon=True).start()
                bot.send_message(ADMIN_ID, "⚙️ جاري تحضير السيرفر...")
            else:
                bot.send_message(ADMIN_ID, "⚠️ المصنع شغال بالفعل!")
        
        elif message.text == "🛑 إيقاف المصنع":
            is_running = False
            bot.send_message(ADMIN_ID, "🛑 تم إيقاف الإنتاج.")

# تشغيل البوت
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
