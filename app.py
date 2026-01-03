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
        
        /* شاشة قفل الدخول */
        .login-screen { position: fixed; inset: 0; background: #000; z-index: 1000; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .login-box { border: 2px solid #00f2ff; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 0 20px #00f2ff; background: rgba(0, 0, 0, 0.9); }
        input { background: #000; border: 1px solid #00f2ff; color: #00f2ff; padding: 12px; text-align: center; font-size: 20px; margin-bottom: 20px; outline: none; border-radius: 5px; width: 250px; }
        
        /* الخلفية (الصورة التي أرسلتها) */
        .hud-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            background: url('https://i.ibb.co/XfXfXfX/hacker-hud.png') no-repeat center;
            background-size: cover;
            display: none;
        }

        .overlay-glass { position: absolute; inset: 0; background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(1px); }

        /* أيقونة الانستقرام الجديدة والمتحركة */
        .insta-float {
            position: absolute; top: 30px; right: 40px;
            display: flex; align-items: center; gap: 12px;
            background: rgba(0, 0, 0, 0.7); padding: 12px 25px;
            border-radius: 50px; border: 2px solid #e1306c;
            color: #fff; font-weight: bold; font-size: 20px;
            text-decoration: none; z-index: 10;
            box-shadow: 0 0 20px #e1306c;
            transition: 0.4s;
            animation: pulse-insta 2s infinite;
        }
        .insta-float:hover { transform: scale(1.1); background: #e1306c; box-shadow: 0 0 40px #e1306c; }
        @keyframes pulse-insta { 0% { box-shadow: 0 0 10px #e1306c; } 50% { box-shadow: 0 0 30px #e1306c; } 100% { box-shadow: 0 0 10px #e1306c; } }

        /* العدادات والأرقام */
        .stats-grid { position: absolute; top: 15%; left: 50%; transform: translateX(-50%); display: flex; gap: 30px; }
        .stat-card { background: rgba(0, 0, 0, 0.8); border: 1px solid #00f2ff; padding: 15px 25px; border-radius: 12px; text-align: center; min-width: 120px; }
        .stat-card span { color: #00f2ff; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
        .stat-card b { display: block; font-size: 32px; color: #ff4500; font-family: 'Courier New', monospace; margin-top: 5px; }

        /* غرفة العمليات */
        .console-room {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            width: 85%; height: 180px; background: rgba(0, 0, 0, 0.85);
            border: 1px solid #00f2ff; border-radius: 8px; padding: 15px;
            overflow-y: auto; color: #00ffaa; font-family: monospace; font-size: 14px;
        }

        /* الأزرار */
        .controls { position: absolute; bottom: 240px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; }
        .btn-v {
            background: rgba(0,0,0,0.8); border: 1px solid #00f2ff; color: #00f2ff;padding: 12px 35px; border-radius: 5px; cursor: pointer; font-weight: bold;
            display: flex; align-items: center; gap: 10px; transition: 0.3s;
        }
        .btn-v:hover { background: #00f2ff; color: #000; box-shadow: 0 0 25px #00f2ff; }
    </style>
</head>
<body>

<div id="login" class="login-screen">
    <div class="login-box">
        <h2 style="color: #00f2ff;">KAIL.911 SYSTEM ACCESS</h2>
        <input type="password" id="passInput" placeholder="PASSWORD (hx888)">
        <br>
        <button class="btn-v" style="position:relative;" onclick="check()">UNLOCK</button>
    </div>
</div>

<div class="hud-container" id="mainPanel">
    <div class="overlay-glass"></div>

    <a href="https://www.instagram.com/kail.911" target="_blank" class="insta-float">
        <i class="fab fa-instagram"></i>
        <span>kail.911</span>
    </a>

    <div class="stats-grid">
        <div class="stat-card"><span>Checked</span><b id="checked">0</b></div>
        <div class="stat-card"><span>Found</span><b id="found" style="color: #0f0;">0</b></div>
        <div class="stat-card"><span>Errors</span><b id="errors" style="color: #f00;">0</b></div>
        <div class="stat-card"><span>Status</span><b id="status" style="font-size: 18px;">READY</b></div>
    </div>

    <div class="controls">
        <button class="btn-v" onclick="run('start')"><i class="fas fa-play"></i> START SCAN</button>
        <button class="btn-v" onclick="run('stop')"><i class="fas fa-stop"></i> STOP SYSTEM</button>
    </div>

    <div class="console-room" id="logs">
        <div>[SYSTEM]: WELCOME KAIL.911 - SYSTEM SECURED.</div>
    </div>
</div>

<script>
    function check() {
        if(document.getElementById('passInput').value === 'hx888') {
            document.getElementById('login').style.display = 'none';
            document.getElementById('mainPanel').style.display = 'block';
        } else { alert('ACCESS DENIED'); }
    }
    function run(c) { $.getJSON('/cmd/' + c); }
    setInterval(() => {
        $.getJSON('/api/stats', (d) => {
            $('#checked').text(d.checked); $('#found').text(d.found); $('#errors').text(d.errors);
            $('#status').text(d.status == "🟢 يعمل" ? "ONLINE" : "OFFLINE");
            let h = ""; d.logs.forEach(l => h += "<div>> " + l + "</div>");
            $('#logs').html(h);
            document.getElementById("logs").scrollTop = document.getElementById("logs").scrollHeight;
        });
    }, 1000);
</script>
</body>
</html>
