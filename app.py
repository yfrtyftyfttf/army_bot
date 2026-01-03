import telebot, requests, os, random, time, threading
from flask import Flask, render_template_string, jsonify

# --- [1] إعدادات الهوية ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

stats = {"checked": 0, "found": 0, "errors": 0, "logs": []}
hunting_active = False

# --- [2] واجهة نظام كاييل المطورة مع ميزة تغيير الخلفية ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نظام كاييل 911 | تحكم كامل</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { background: #000; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: 'Segoe UI', sans-serif; overflow: hidden; }
        
        /* الحاوية الرئيسية مع ميزة تغيير الخلفية برمجياً */
        .main-container {
            position: relative; width: 950px; height: 650px;
            background: url('https://w0.peakpx.com/wallpaper/599/471/wallpaper-anonymous-hacker-dark-background-mask-neon-light.jpg') no-repeat center;
            background-size: cover; border: 2px solid #00f2ff; box-shadow: 0 0 30px #00f2ff66; border-radius: 10px; display: none;
            transition: background 0.5s ease-in-out;
        }

        .overlay { position: absolute; inset: 0; background: rgba(0, 0, 0, 0.75); border-radius: 8px; }

        /* شاشة الدخول */
        .gate { position: fixed; inset: 0; background: #000; z-index: 1000; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .gate input { background: transparent; border: 1px solid #00f2ff; color: #00f2ff; padding: 15px; text-align: center; border-radius: 5px; outline: none; font-size: 20px; width: 300px; }

        /* مركز التحكم بالخلفية */
        .bg-control { position: absolute; top: 25px; left: 25px; z-index: 20; }
        .upload-btn { background: rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; color: #00f2ff; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 12px; transition: 0.3s; }
        .upload-btn:hover { background: #00f2ff; color: #000; }
        #imageInput { display: none; }

        /* معلومات المطور */
        .user-panel { position: absolute; top: 25px; right: 25px; display: flex; flex-direction: column; align-items: flex-end; gap: 10px; z-index: 10; }
        .insta-link { background: rgba(225, 48, 108, 0.2); border: 1px solid #e1306c; color: #fff; text-decoration: none; padding: 10px 20px; border-radius: 50px; font-size: 14px; display: flex; align-items: center; gap: 10px; box-shadow: 0 0 15px #e1306c; }

        /* العدادات وشاشة الهجوم */
        .stats-display { position: absolute; top: 130px; width: 100%; display: flex; justify-content: center; gap: 30px; z-index: 10; }
        .stat-card { background: rgba(0, 0, 0, 0.85); border: 1px solid #00f2ff; padding: 20px; border-radius: 10px; text-align: center; min-width: 160px; }
        .stat-card b { font-size: 35px; color: #ff4500; font-family: monospace; }

        .attack-console { position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); width: 85%; height: 200px; background: rgba(0, 0, 0, 0.9); border: 1px solid #00f2ff; padding: 15px; overflow-y: auto; color: #00ffaa; font-family: monospace; font-size: 14px; direction: ltr; z-index: 10; }

        .action-bar { position: absolute; bottom: 270px; width: 100%; display: flex; justify-content: center; gap: 20px; z-index: 10; }
        .btn-style { background: rgba(0, 242, 255, 0.1); border: 2px solid #00f2ff; color: #00f2ff; padding: 12px 45px; cursor: pointer; border-radius: 5px; font-weight: bold; transition: 0.3s; }
        .btn-style:hover { background: #00f2ff; color: #000; }
    </style>
</head>
<body>

<div id="gate" class="gate">
    <h1 style="color:#00f2ff">نظام KAIL.911</h1>
    <input type="password" id="pass" placeholder="أدخل كلمة السر">
    <br>
    <button class="btn-style" onclick="enter()">دخول</button>
</div>

<div class="main-container" id="mainPanel">
    <div class="overlay"></div>

    <div class="bg-control">
        <label for="imageInput" class="upload-btn">
            <i class="fas fa-image"></i> تغيير صورة الخلفية
        </label>
        <input type="file" id="imageInput" accept="image/*">
    </div>

    <audio id="hackerMusic" loop>
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-15.mp3" type="audio/mpeg">
    </audio>

    <div class="user-panel">
        <span style="color: #00f2ff; font-weight: bold; font-size: 18px;">القائد: kail.911</span>
        <a href="https://www.instagram.com/kail.911" target="_blank" class="insta-link">
            <i class="fab fa-instagram"></i> حسابي الرسمي
        </a>
    </div>

    <div class="stats-display">
        <div class="stat-card"><span>المفحوص</span><b id="c">0</b></div>
        <div class="stat-card"><span>المصيد</span><b id="f" style="color:#0f0">0</b></div>
        <div class="stat-card"><span>الأخطاء</span><b id="e" style="color:#f00">0</b></div>
    </div>

    <div class="action-bar">
        <button class="btn-style" onclick="run('start')">بدء الهجوم</button>
        <button class="btn-style" onclick="run('stop')" style="border-color:#f00; color:#f00;">إيقاف</button>
    </div>

    <div class="attack-console" id="log-box"></div>
</div>

<script>
    // نظام تغيير الخلفية
    document.getElementById('imageInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                document.getElementById('mainPanel').style.backgroundImage = url('${event.target.result}');
            };
            reader.readAsDataURL(file);
        }
    });

    function enter() { 
        if(document.getElementById('pass').value === 'hx888') {
            $('#gate').fadeOut(500);
            $('#mainPanel').fadeIn(1000);
            document.getElementById('hackerMusic').play();
        } else { alert('خطأ!'); } 
    }
    
    function run(c) { $.getJSON('/cmd/'+c); }

    setInterval(() => {
        $.getJSON('/api/stats', (d) => {
            $('#c').text(d.checked); $('#f').text(d.found); $('#e').text(d.errors);
            let h = ""; d.logs.forEach(l => h += "<div>[LOG]> "+l+"</div>");
            $('#log-box').html(h);
            document.getElementById("log-box").scrollTop = 9999;
        });
    }, 1000);
</script>
</body>
</html>
