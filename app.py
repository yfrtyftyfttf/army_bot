import telebot, requests, os, random, time, threading
from flask import Flask, render_template_string, jsonify
from datetime import datetime

# --- [ الإعدادات ] ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- [ قسم البروكسيات ] ---
RAW_PROXIES = """
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
