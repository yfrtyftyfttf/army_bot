import telebot, requests, os, random, time, threading
from flask import Flask, render_template_string, jsonify
from datetime import datetime

# --- [ الإعدادات ] ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- [ قسم البروكسيات ] ---
RAW_PROXIES = """
ضع البروكسيات هنا (كل واحد في سطر)
"""
PROXIES_LIST = [p.strip() for p in RAW_PROXIES.strip().split('\n') if p.strip()]

# --- [ البيانات ] ---
stats = {"checked": 0, "found": 0, "errors": 0, "logs": []}
found_accounts = [] # لتخزين الحسابات المصادة
hunting_active = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <div class="stat-card">ERRORS<b id="e" style="color:red">0</b></div>
    </div>

    <div class="action-bar ui-element">
        <button class="btn" onclick="run('start')"><i class="fas fa-play"></i> START</button>
        <button class="btn" onclick="run('stop')" style="border-color:red;color:red"><i class="fas fa-stop"></i> STOP</button>
        <button class="btn" onclick="openHits()" style="border-color:#0f0;color:#0f0"><i class="fas fa-briefcase"></i> HITS</button>
    </div>

    <div class="console ui-element" id="log-box"></div>

    <div id="hits-modal">
        <span class="close-hits" onclick="closeHits()">&times;</span>
        <h2 style="color:#0f0; text-align:center;"><i class="fas fa-trophy"></i> ACCOUNTS CAPTURED</h2>
        <div class="hits-list" id="hits-content">
            </div>
    </div>
</div>

<script>
    const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");
    canvas.width = 950; canvas.height = 650;
    const chars = "01KAIL911";
    const drops = Array(Math.floor(canvas.width/16)).fill(1);
    function draw() {
        ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle = "#00f2ff"; ctx.font = "15px monospace";
        drops.forEach((y, i) => {
            ctx.fillText(chars[Math.floor(Math.random()*chars.length)], i*16, y*16);
            if(y*16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        });
    }
    setInterval(draw, 50);

    function enter() { if(document.getElementById("pass").value === "hx888") { $("#gate").fadeOut(); $("#mainPanel").fadeIn(); } else { alert("ACCESS DENIED"); } }
    function run(c) { $.getJSON("/cmd/"+c); }
    function openHits() {
        $.getJSON("/api/hits", (data) => {
            let html = "";
            if(data.length === 0) html = "<div style='text-align:center; padding:20px;'>No Accounts Found Yet...</div>";
            data.forEach(acc => {
                html += <div class="hit-item"><span>@${acc.user}</span><span>${acc.time}</span></div>;
            });
            $("#hits-content").html(html);
            $("#hits-modal").fadeIn();
        });
    }
    function closeHits() { $("#hits-modal").fadeOut(); }

    setInterval(() => {
        $.getJSON("/api/stats", (d) => {
            $("#c").text(d.checked); $("#f").text(d.found); $("#e").text(d.errors);
            let h = ""; d.logs.forEach(l => h += "<div>> "+l+"</div>");
            $("#log-box").html(h); document.getElementById("log-box").scrollTop = 9999;
        });
    }, 1000);
</script>
</body>
</html>
"""

@app.route("/")
def index(): return render_template_string(HTML_TEMPLATE)

@app.route("/api/stats")
def stats_api(): return jsonify(stats)

@app.route("/api/hits")
def hits_api(): return jsonify(found_accounts)

@app.route("/cmd/<c>")
def cmd(c):
    global hunting_active
    if c == "start":
        if not hunting_active:
            hunting_active = True
            threading.Thread(target=real_hunt, daemon=True).start()
    elif c == "stop": hunting_active = False
    return jsonify(ok=True)

def real_hunt():
    while hunting_active:
        # توليد يوزر 4 أحرف
        user = "".join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890._") for _ in range(4))
        url = f"https://www.instagram.com/{user}/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        px = {}
        if PROXIES_LIST:
            p = random.choice(PROXIES_LIST)
            if not p.startswith('http'): p = 'http://' + p
            px = {"http": p, "https": p}
        
        try:
            response = requests.get(url, headers=headers, proxies=px, timeout=5)
            stats["checked"] += 1
            if response.status_code == 404:
                stats["found"] += 1
                now = datetime.now().strftime("%H:%M:%S")
                # إضافة للقائمة الداخلية
                found_accounts.append({"user": user, "time": now})
                msg = f"🔥 [HIT] Available: @{user}"
                stats["logs"].append(msg)
                bot.send_message("-1002361139454", msg)
            else:
                stats["logs"].append(f"Scanning @{user}...")
        except:
            stats["errors"] += 1
            stats["logs"].append(f"[!] Proxy Error - Skipping...")
        
        if len(stats["logs"]) > 15: stats["logs"].pop(0)
        time.sleep(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    <title>KAIL.911 ULTRA HUNTER</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { margin: 0; background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: monospace; overflow: hidden; }
        .main-container { position: relative; width: 950px; height: 650px; border: 2px solid #00f2ff; border-radius: 15px; box-shadow: 0 0 35px #00f2ff99; display: none; }
        #matrix { position: absolute; inset: 0; z-index: 1; }
        .overlay { position: absolute; inset: 0; background: rgba(0, 0, 0, 0.8); z-index: 2; }
        .ui-element { position: relative; z-index: 3; }
        .stats-display { position: absolute; top: 110px; width: 100%; display: flex; justify-content: center; gap: 20px; }
        .stat-card { background: rgba(0, 10, 20, 0.9); border: 1px solid #00f2ff; padding: 15px; border-radius: 10px; min-width: 140px; text-align: center; color: #00f2ff; }
        .stat-card b { font-size: 30px; display: block; color: #0f0; }
        .action-bar { position: absolute; bottom: 250px; width: 100%; display: flex; justify-content: center; gap: 15px; }
        .btn { background: rgba(0, 242, 255, 0.1); border: 1px solid #00f2ff; color: #00f2ff; padding: 10px 25px; cursor: pointer; border-radius: 5px; font-weight: bold; transition: 0.3s; }
        .btn:hover { background: #00f2ff; color: #000; box-shadow: 0 0 15px #00f2ff; }
        .console { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); width: 90%; height: 180px; background: rgba(0, 5, 10, 0.95); border: 1px solid #00f2ff; padding: 10px; overflow-y: auto; color: #00ffaa; font-size: 13px; text-align: left; direction: ltr; }
        
        /* شاشة الحسابات المصادة */
        #hits-modal { display: none; position: absolute; inset: 20px; background: #000; border: 2px solid #0f0; z-index: 100; border-radius: 15px; box-shadow: 0 0 50px #0f0; padding: 20px; }
        .hits-list { height: 85%; overflow-y: auto; border-top: 1px solid #0f0; margin-top: 10px; padding-top: 10px; }
        .hit-item { border-bottom: 1px dashed #0f0; padding: 8px; display: flex; justify-content: space-between; color: #0f0; }
        .close-hits { position: absolute; top: 10px; right: 20px; color: red; cursor: pointer; font-size: 25px; }
        
        .gate { position: fixed; inset: 0; background: #000; z-index: 999; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .gate input { background: transparent; border: 1px solid #00f2ff; color: #00f2ff; padding: 15px; font-size: 20px; text-align: center; outline: none; }
    </style>
</head>
<body>

<div class="gate" id="gate">
    <h1 style="color:#00f2ff; letter-spacing: 5px;">KAIL.911 SYSTEM</h1>
    <input type="password" id="pass" placeholder="ACCESS CODE">
    <br>
    <button class="btn" onclick="enter()">UNLOCK</button>
</div>

<div class="main-container" id="mainPanel">
    <canvas id="matrix"></canvas>
    <div class="overlay"></div>
    
    <div class="stats-display ui-element">
        <div class="stat-card">CHECKED<b id="c">0</b></div>
        <div class="stat-card">FOUND<b id="f" style="color:#0f0">0</b></div>
