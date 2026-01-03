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

# --- [2] واجهة الموقع HUD الاحترافية ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>KAIL.911 | HACKER SYSTEM</title>
    <link rel="icon" href="https://img.icons8.com/neon/96/hacker.png" type="image/png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { background: #000; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
        
        .login-screen { position: fixed; inset: 0; background: #000; z-index: 1000; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .login-box { border: 2px solid #00f2ff; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 0 20px #00f2ff; background: rgba(0, 0, 0, 0.9); }
        input { background: #000; border: 1px solid #00f2ff; color: #00f2ff; padding: 12px; text-align: center; font-size: 20px; margin-bottom: 20px; outline: none; border-radius: 5px; width: 250px; }
        
        .hud-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            background: url('https://i.ibb.co/3YYv0Xm/hacker-bg.jpg') no-repeat center;
            background-size: cover;
            display: none;
        }

        .overlay-glass { position: absolute; inset: 0; background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(2px); }

        /* أيقونة الانستقرام ورابط الحساب */
        .insta-link {
            position: absolute; top: 25px; right: 25px;
            display: flex; align-items: center; gap: 10px;
            background: rgba(0, 0, 0, 0.8); border: 2px solid #e1306c;
            padding: 10px 20px; border-radius: 50px;
            color: #fff; text-decoration: none; font-weight: bold;
            box-shadow: 0 0 15px #e1306c; transition: 0.3s; z-index: 100;
        }
        .insta-link:hover { transform: scale(1.05); background: #e1306c; }

        .stats-hud { position: absolute; top: 10%; width: 100%; display: flex; justify-content: center; gap: 20px; }
        .stat-item { background: rgba(0, 0, 0, 0.8); border: 1px solid #00f2ff; padding: 15px 30px; border-radius: 10px; text-align: center; min-width: 120px; }
        .stat-item span { color: #00f2ff; font-size: 12px; display: block; }
        .stat-item b { font-size: 30px; color: #ff4500; font-family: monospace; }

        .console-box {
            position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
            width: 90%; height: 200px; background: rgba(0,0,0,0.85);
            border: 1px solid #00f2ff; border-radius: 5px; padding: 15px;
            overflow-y: auto; color: #00ffaa; font-family: monospace; font-size: 13px;
        }

        .controls-hud { position: absolute; bottom: 250px; left: 50%; transform: translateX(-50%); display: flex; gap: 15px; }
        .btn-action {
            background: rgba(0,0,0,0.7); border: 1px solid #00f2ff; color: #00f2ff;
            padding: 12px 30px; cursor: pointer; border-radius: 4px; font-weight: bold;
            display: flex; align-items: center; gap: 8px; transition: 0.3s;
        }
        .btn-action:hover { background: #00f2ff; color: #000; box-shadow: 0 0 20px #00f2ff; }
    </style>
</head>
<body>

<div id="login" class="login-screen">
    <div class="login-box">
        <h2 style="color: #00f2ff;">KAIL.911 SECURITY</h2>
        <input type="password" id="passInput" placeholder="CODE (hx888)">
        <br>
        <button class="btn-action" style="position:relative;" onclick="check()">ACCESS SYSTEM</button>
    </div>
</div>

<div class="hud-container" id="mainPanel">
    <div class="overlay-glass"></div>

    <a href="https://www.instagram.com/kail.911" target="_blank" class="insta-link">
        <i class="fab fa-instagram"></i>
        <span>INSTA: kail.911</span>
    </a>

    <div class="stats-hud">
        <div class="stat-item"><span>CHECKED</span><b id="checked">0</b></div>
        <div class="stat-item"><span>FOUND</span><b id="found" style="color:#0f0">0</b></div>
        <div class="stat-item"><span>ERRORS</span><b id="errors" style="color:#f00">0</b></div>
    </div>

    <div class="controls-hud">
        <button class="btn-action" onclick="run('start')"><i class="fas fa-play"></i> START</button>
        <button class="btn-action" onclick="run('stop')"><i class="fas fa-stop"></i> STOP</button>
    </div>

    <div class="console-box" id="logs">
        <div>[SYSTEM]: INITIALIZING... OK.</div>
    </div>
</div>

<script>
    function check() {
        if(document.getElementById('passInput').value === 'hx888') {
            document.getElementById('login').style.display = 'none';
            document.getElementById('mainPanel').style.display = 'block';
        } else { alert('WRONG CODE'); }
    }
    function run(c) { $.getJSON('/cmd/' + c); }
    setInterval(() => {
        $.getJSON('/api/stats', (d) => {
            $('#checked').text(d.checked); $('#found').text(d.found); $('#errors').text(d.errors);
            let h = ""; d.logs.forEach(l => h += "<div>> " + l + "</div>");
            $('#logs').html(h);
            document.getElementById("logs").scrollTop = document.getElementById("logs").scrollHeight;
        });
    }, 1000);
</script>
</body>
</html>
"""

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
            threading.Thread(target=hunt).start()
    elif c == 'stop': hunting_active = False
    return jsonify({"ok": True})

def hunt():
    while hunting_active:
        user = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))
        stats['checked'] += 1
        stats['logs'].append(f"SCANNING: @{user}")
        if len(stats['logs']) > 30: stats['logs'].pop(0)
        time.sleep(0.5)

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling()).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
