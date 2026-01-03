import telebot
import requests
import os
import random
import time
import threading
from flask import Flask, render_template_string, jsonify

# --- [1] إعدادات الهوية ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
ADMIN_ID = 6695916631 

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# بيانات السيرفر الحية
stats = {
    "checked": 0, 
    "found": 0, 
    "errors": 0, 
    "last_user": "None",
    "status": "🔴 متوقف",
    "logs": []
}
hunting_active = False

# --- [2] تصميم واجهة الموقع (التصميم الذي أرسلته) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>A7MED HUNTER PANEL</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { background: #010b14; color: #00f2ff; font-family: 'Courier New', monospace; text-align: center; margin: 0; overflow-x: hidden; }
        .overlay { position: fixed; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 1000; display: flex; justify-content: center; align-items: center; flex-direction: column; }
        .panel { border: 2px solid #00f2ff; padding: 20px; display: inline-block; background: rgba(0, 20, 40, 0.8); box-shadow: 0 0 20px #00f2ff; border-radius: 10px; margin-top: 50px; width: 80%; max-width: 800px; }
        .header { font-size: 24px; border-bottom: 1px solid #00f2ff; margin-bottom: 20px; padding-bottom: 10px; }
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .stat-card { border: 1px solid #006677; padding: 15px; border-radius: 5px; background: rgba(0, 255, 255, 0.05); }
        .btn-group { display: flex; justify-content: space-around; margin-top: 20px; }
        button { background: transparent; border: 1px solid #00f2ff; color: #00f2ff; padding: 10px 20px; cursor: pointer; transition: 0.3s; font-weight: bold; }
        button:hover { background: #00f2ff; color: #000; }
        .console { background: #000; border: 1px solid #006677; height: 150px; overflow-y: auto; text-align: left; padding: 10px; font-size: 12px; color: #0f0; margin-top: 20px; }
        .logo { width: 100px; margin-bottom: 10px; filter: drop-shadow(0 0 5px #00f2ff); }
    </style>
</head>
<body>

<div id="welcome" class="overlay">
    <h1>أهلاً بك معك الرد التلقائي من المبرمج محمد kail.911</h1>
    <button onclick="enterPanel()">دخول غرفة العمليات</button>
</div>

<div class="panel">
    <div class="header">A7MED HUNTER PANEL - kail.911</div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div>🔍 المجموع المفحوص</div>
            <h2 id="checked">0</h2>
        </div>
        <div class="stat-card">
            <div>🎯 الصيد الثمين</div>
            <h2 id="found" style="color: #0f0;">0</h2>
        </div>
        <div class="stat-card">
            <div>⚠️ أخطاء</div>
            <h2 id="errors" style="color: #f00;">0</h2>
        </div>
        <div class="stat-card">
            <div>📡 الحالة</div>
            <h2 id="status">🔴 متوقف</h2>
        </div>
    </div>

    <div class="btn-group">
        <button onclick="sendCommand('start')">1️⃣ صيد</button>
        <button onclick="sendCommand('stop')">2️⃣ توقف</button>
        <button onclick="toggleConsole()">3️⃣ غرفة العمليات</button>
    </div>

    <div id="console_box" class="console" style="display: none;">
        <div>--- نظام الصيد التلقائي جاهز ---</div>
        <div id="logs"></div>
    </div>
</div>

<script>
    function enterPanel() { document.getElementById('welcome').style.display = 'none'; }
    function toggleConsole() { $('#console_box').toggle(); }

    function sendCommand(cmd) {
        $.getJSON('/command/' + cmd, function(data) { alert(data.msg); });
    }

    function updateStats() {
        $.getJSON('/api/stats', function(data) {
            $('#checked').text(data.checked);
            $('#found').text(data.found);
            $('#errors').text(data.errors);
            $('#status').text(data.status);
            
            let logHtml = "";
            data.logs.
            forEach(l => logHtml += "<div>" + l + "</div>");
            $('#logs').html(logHtml);
            
            // التمرير لأسفل الكونسول تلقائياً
            var objDiv = document.getElementById("console_box");
            objDiv.scrollTop = objDiv.scrollHeight;
        });
    }
    setInterval(updateStats, 1000);
</script>
</body>
</html>
"""

# --- [3] منطق البوت والصيد ---
def add_log(msg):
    stats['logs'].append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(stats['logs']) > 20: stats['logs'].pop(0)

def hunting_loop():
    global hunting_active
    while hunting_active:
        user = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890._') for i in range(random.randint(4,8)))
        stats['checked'] += 1
        add_log(f"فحص: @{user}...")
        
        # محاكاة الفحص (ضع هنا كود requests الفعلي مع البروكسي)
        try:
            # مثال: ريكويست بسيط
            time.sleep(0.5) 
        except: stats['errors'] += 1
        
        if not hunting_active: break

# --- [4] مسارات الموقع (Web Routes) ---
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats():
    return jsonify(stats)

@app.route('/command/<cmd>')
def run_command(cmd):
    global hunting_active
    if cmd == 'start':
        if not hunting_active:
            hunting_active = True
            stats['status'] = "🟢 يعمل"
            threading.Thread(target=hunting_loop).start()
            return jsonify({"msg": "تم بدء الصيد أستاذ محمد"})
    elif cmd == 'stop':
        hunting_active = False
        stats['status'] = "🔴 متوقف"
        return jsonify({"msg": "تم إيقاف النظام"})
    return jsonify({"msg": "أمر غير معروف"})

# --- [5] تشغيل كل شيء ---
if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
