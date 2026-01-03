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

stats = {"checked": 0, "found": 0, "errors": 0, "status": "🔴 متوقف", "logs": []}
hunting_active = False

# --- [2] واجهة الموقع HUD مع قفل الحماية ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>KAIL.911 | HUD SYSTEM</title>
    <link rel="icon" href="https://img.icons8.com/neon/96/hacker.png" type="image/png">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { background: #000; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: sans-serif; }
        
        .hud-wrapper {
            position: relative;
            width: 800px;
            height: 800px;
            background: url('https://r.jina.ai/i/e0a0250630b9437b98547214e2162f4e') no-repeat center;
            background-size: contain;
            display: none; /* مخفي حتى إدخال الرمز */
        }

        .stat-value { position: absolute; font-family: monospace; font-weight: bold; color: #ff4500; font-size: 28px; }
        #checked { top: 275px; left: 365px; } 
        #found { top: 275px; left: 510px; } 
        #errors { top: 435px; left: 440px; color: #00f2ff; }
        #status { top: 275px; left: 140px; font-size: 16px; color: #00f2ff; }

        .console-box { position: absolute; bottom: 110px; left: 95px; width: 615px; height: 140px; color: #00f2ff; font-size: 12px; text-align: left; overflow-y: auto; }
        
        .hidden-btn { position: absolute; background: rgba(0,242,255,0.05); border: 1px solid rgba(0,242,255,0.2); color: #00f2ff; cursor: pointer; }
        #btn-start { bottom: 335px; left: 120px; width: 185px; height: 40px; }
        #btn-stop { bottom: 335px; left: 350px; width: 185px; height: 40px; }
        #btn-logs { bottom: 335px; left: 580px; width: 185px; height: 40px; }

        /* شاشة قفل الدخول */
        .login-screen {
            position: fixed; inset: 0; background: #000; z-index: 1000;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }
        .login-box { border: 2px solid #00f2ff; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 0 20px #00f2ff; }
        input { background: #000; border: 1px solid #00f2ff; color: #00f2ff; padding: 10px; text-align: center; font-size: 20px; margin-bottom: 20px; outline: none; }
    </style>
</head>
<body>

<div id="login" class="login-screen">
    <div class="login-box">
        <h2 style="color: #00f2ff;">نظام KAIL.911 المحمي</h2>
        <p style="color: #fff;">أهلاً بك أستاذ محمد، يرجى إدخال رمز الدخول</p>
        <input type="password" id="passInput" placeholder="ENTER CODE">
        <br>
        <button class="hidden-btn" style="position:relative; width: 150px; height: 40px;" onclick="checkPass()">دخول</button>
    </div>
</div>

<div class="hud-wrapper" id="mainPanel">
    <div id="status" class="stat-value">🔴</div>
    <div id="checked" class="stat-value">0</div>
    <div id="found" class="stat-value">0</div>
    <div id="errors" class="stat-value">0</div>

    <div class="console-box" id="console"></div>

    <button id="btn-start" class="hidden-btn" onclick="sendCmd('start')">1️⃣ صيد</button>
    <button id="btn-stop" class="hidden-btn" onclick="sendCmd('stop')">2️⃣ توقف</button>
    <button id="btn-logs" class="hidden-btn" onclick="toggleConsole()">3️⃣ غرفة العمليات</button>
</div>

<script>
    function checkPass() {
        const pass = document.getElementById('passInput').value;
        if(pass === 'hx888') {
            document.getElementById('login').style.display = 'none';
            document.getElementById('mainPanel').style.display = 'block';
        } else {
            alert('الرمز خطأ! حاول مجدداً أستاذ محمد');
            }
    }
    
    function sendCmd(c) { $.getJSON('/cmd/' + c); }
    function toggleConsole() { $('#console').fadeToggle(); }

    setInterval(function update() {
        $.getJSON('/api/stats', function(data) {
            $('#checked').text(data.checked);
            $('#found').text(data.found);
            $('#errors').text(data.errors);
            $('#status').text(data.status == "🟢 يعمل" ? "🟢" : "🔴");
            let html = "";
            data.logs.forEach(l => html += "<div>[#] " + l + "</div>");
            $('#console').html(html);
            document.getElementById("console").scrollTop = document.getElementById("console").scrollHeight;
        });
    }, 1000);
</script>
</body>
</html>
"""

# --- [3] المنطق البرمجي (نفس السابق مع استمرار العمل) ---
@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def get_stats(): return jsonify(stats)

@app.route('/cmd/<c>')
def run_cmd(c):
    global hunting_active
    if c == 'start':
        if not hunting_active:
            hunting_active = True
            stats['status'] = "🟢 يعمل"
            threading.Thread(target=hunt_loop).start()
    elif c == 'stop':
        hunting_active = False
        stats['status'] = "🔴 متوقف"
    return jsonify({"ok": True})

def hunt_loop():
    while hunting_active:
        user = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))
        stats['checked'] += 1
        stats['logs'].append(f"فحص يوزر: @{user}")
        if len(stats['logs']) > 30: stats['logs'].pop(0)
        time.sleep(0.5)

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
