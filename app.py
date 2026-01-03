import telebot, os, random, time, threading
from flask import Flask, render_template_string, jsonify

# --- [ الإعدادات ] ---
BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

stats = {"checked": 0, "found": 0, "errors": 0, "logs": []}
hunting_active = False

# --- [ واجهة النظام ] ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>KAIL.911 SYSTEM</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { margin: 0; background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: monospace; overflow: hidden; }
        .main-container { position: relative; width: 950px; height: 650px; border: 2px solid #00f2ff; border-radius: 15px; box-shadow: 0 0 35px #00f2ff99; display: none; overflow: hidden; }
        #matrix { position: absolute; inset: 0; z-index: 1; }
        .overlay { position: absolute; inset: 0; background: rgba(0, 0, 0, 0.75); z-index: 2; }
        .ui-element { position: relative; z-index: 3; }
        .user-panel { position: absolute; top: 25px; right: 25px; z-index: 10; }
        .insta-btn { color: #fff; text-decoration: none; font-weight: bold; background: rgba(225, 48, 108, 0.3); border: 1px solid #e1306c; padding: 10px 20px; border-radius: 50px; display: flex; align-items: center; gap: 8px; box-shadow: 0 0 15px #e1306c; }
        .stats-display { position: absolute; top: 130px; width: 100%; display: flex; justify-content: center; gap: 30px; }
        .stat-card { background: rgba(0, 0, 0, 0.9); border: 1px solid #00f2ff; padding: 20px; border-radius: 10px; min-width: 160px; text-align: center; color: #00f2ff; }
        .stat-card b { font-size: 35px; display: block; color: #0f0; }
        .action-bar { position: absolute; bottom: 270px; width: 100%; display: flex; justify-content: center; gap: 20px; }
        .btn { background: rgba(0, 242, 255, 0.1); border: 2px solid #00f2ff; color: #00f2ff; padding: 12px 45px; cursor: pointer; border-radius: 6px; font-weight: bold; }
        .attack-console { position: absolute; bottom: 35px; left: 50%; transform: translateX(-50%); width: 85%; height: 200px; background: rgba(0, 0, 0, 0.95); border: 1px solid #00f2ff; padding: 15px; overflow-y: auto; color: #00ffaa; font-size: 14px; direction: ltr; }
        .gate { position: fixed; inset: 0; background: #000; z-index: 999; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .gate input { background: transparent; border: 1px solid #00f2ff; color: #00f2ff; padding: 15px; font-size: 20px; text-align: center; border-radius: 6px; outline: none; width: 300px; }
    </style>
</head>
<body>
<div class="gate" id="gate">
    <h1 style="color:#00f2ff">KAIL.911 SYSTEM</h1>
    <input type="password" id="pass" placeholder="PASSWORD">
    <br><br>
    <button class="btn" onclick="enter()">LOGIN</button>
</div>
<div class="main-container" id="mainPanel">
    <canvas id="matrix"></canvas>
    <div class="overlay"></div>
    <div class="user-panel ui-element">
        <a href="https://www.instagram.com/kail.911" target="_blank" class="insta-btn"><i class="fab fa-instagram"></i> kail.911</a>
    </div>
    <div class="stats-display ui-element">
        <div class="stat-card">CHECKED<b id="c">0</b></div>
        <div class="stat-card">FOUND<b id="f">0</b></div>
        <div class="stat-card">ERRORS<b id="e" style="color:red">0</b></div>
    </div>
    <div class="action-bar ui-element">
        <button class="btn" onclick="run('start')">START</button>
        <button class="btn" onclick="run('stop')" style="border-color:red;color:red">STOP</button>
    </div>
    <div class="attack-console ui-element" id="log-box"></div>
</div>
<script>
    const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");
    canvas.width = 950; canvas.
    height = 650;
    const chars = "01KAIL911";
    const drops = Array(Math.floor(canvas.width/16)).fill(1);
    function draw() {
        ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle = "#00f2ff"; ctx.font = "16px monospace";
        drops.forEach((y, i) => {
            ctx.fillText(chars[Math.floor(Math.random()*chars.length)], i*16, y*16);
            if(y*16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        });
    }
    setInterval(draw, 50);
    function enter() { if(document.getElementById("pass").value === "hx888") { $("#gate").hide(); $("#mainPanel").show(); } else { alert("WRONG!"); } }
    function run(c) { $.getJSON("/cmd/"+c); }
    setInterval(() => {
        $.getJSON("/api/stats", (d) => {
            $("#c").text(d.checked); $("#f").text(d.found); $("#e").text(d.errors);
            let h = ""; d.logs.forEach(l => h += "<div>[SYSTEM] "+l+"</div>");
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

@app.route("/cmd/<c>")
def cmd(c):
    global hunting_active
    if c == "start":
        if not hunting_active:
            hunting_active = True
            threading.Thread(target=hunt, daemon=True).start()
    elif c == "stop": hunting_active = False
    return jsonify(ok=True)

def hunt():
    while hunting_active:
        u = "".join(random.choice("abcdef12345") for _ in range(5))
        stats["checked"] += 1
        stats["logs"].append(f"Scanning: @{u}")
        if len(stats["logs"]) > 20: stats["logs"].pop(0)
        time.sleep(0.5)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
