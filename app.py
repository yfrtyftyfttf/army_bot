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

# --- [2] واجهة الموقع HUD المدمجة بالأيقونة والتصميم ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>KAIL.911 | HUD SYSTEM</title>
    
    <link rel="icon" href="https://img.icons8.com/neon/96/hacker.png" type="image/png">
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { background: #000; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        
        /* تصميم الخلفية باستخدام الصورة التي اخترتها */
        .hud-wrapper {
            position: relative;
            width: 800px;
            height: 800px;
            background: url('https://r.jina.ai/i/e0a0250630b9437b98547214e2162f4e') no-repeat center;
            background-size: contain;
        }

        /* توزيع الأرقام فوق الأيقونات في الصورة */
        .stat-value {
            position: absolute;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #ff4500; /* لون برتقالي مثل الصورة */
            font-size: 28px;
        }

        #checked { top: 275px; left: 365px; } 
        #found { top: 275px; left: 510px; } 
        #errors { top: 435px; left: 440px; color: #00f2ff; }
        #status { top: 275px; left: 140px; font-size: 16px; color: #00f2ff; }

        /* منطقة غرفة العمليات */
        .console-box {
            position: absolute;
            bottom: 110px;
            left: 95px;
            width: 615px;
            height: 140px;
            background: transparent;
            overflow-y: auto;
            padding: 10px;
            font-size: 12px;
            color: #00f2ff;
            text-align: left;
        }

        .log-line { margin-bottom: 3px; border-left: 1px solid #00f2ff; padding-left: 5px; }

        /* أزرار شفافة فوق أزرار الصورة لتعمل عند اللمس */
        .hidden-btn {
            position: absolute;
            background: rgba(0,242,255,0.05);
            border: 1px solid rgba(0,242,255,0.2);
            color: #00f2ff;
            cursor: pointer;
            border-radius: 5px;
            transition: 0.2s;
        }
        .hidden-btn:hover { background: rgba(0,242,255,0.2); }

        #btn-start { bottom: 335px; left: 120px; width: 185px; height: 40px; }
        #btn-stop { bottom: 335px; left: 350px; width: 185px; height: 40px; }
        #btn-logs { bottom: 335px; left: 580px; width: 185px; height: 40px; }

        /* شاشة الترحيب */
        .overlay {
            position: fixed; inset: 0; background: #000; z-index: 100;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }
    </style>
</head>
<body>

<div id="welcome" class="overlay">
    <h2 style="color: #00f2ff; font-family: 'Arial'; text-shadow: 0 0 10px #00f2ff;">اهلا بك معك الرد التلقائي من المبرمج محمد kail.911</h2>
    <button class="hidden-btn" style="position:relative; width: 220px; height: 50px;" onclick="hideWelcome()">📡 دخول غرفة العمليات</button>
</div>

<div class="hud-wrapper">
    <div id="status" class="stat-value">🔴</div>
    <div id="checked" class="stat-value">0</div>
    <div id="found" class="stat-value">0</div>
    <div id="errors" class="stat-value">0</div>

    <div class="console-box" id="console">
        <div class="log-line">SYSTEM STATUS: READY [kail.911]</div>
    </div>

    <button id="btn-start" class="hidden-btn" onclick="sendCmd('start')">1️⃣ صيد</button>
    <button id="btn-stop" class="hidden-btn" onclick="sendCmd('stop')">2️⃣ توقف</button>
    <button id="btn-logs" class="hidden-btn" onclick="toggleConsole()">3️⃣ غرفة العمليات</button>
</div>
<script>
    function hideWelcome() { document.getElementById('welcome').style.opacity = '0'; setTimeout(()=> {document.getElementById('welcome').style.display='none'}, 500); }
    function toggleConsole() { $('#console').fadeToggle(); }
    function sendCmd(c) { $.getJSON('/cmd/' + c); }

    function update() {
        $.getJSON('/api/stats', function(data) {
            $('#checked').text(data.checked);
            $('#found').text(data.found);
            $('#errors').text(data.errors);
            $('#status').text(data.status == "🟢 يعمل" ? "🟢" : "🔴");
            
            let html = "";
            data.logs.forEach(l => html += "<div class='log-line'>[PROCESS]: " + l + "</div>");
            $('#console').html(html);
            var d = document.getElementById("console");
            d.scrollTop = d.scrollHeight;
        });
    }
    setInterval(update, 1000);
</script>
</body>
</html>
