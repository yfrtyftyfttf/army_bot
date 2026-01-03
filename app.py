import telebot, os, random, time, threading
from flask import Flask, render_template_string, jsonify

BOT_TOKEN = "8255141449:AAGu30tB0cY68YMkBOkW6pGr1owhyqeaPGE"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

stats = {"checked": 0, "found": 0, "errors": 0, "logs": []}
hunting_active = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>KAIL.911 OPERATIONS</title>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<style>
body{
    margin:0;
    background:#000;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    font-family:monospace;
    overflow:hidden;
}

.main-container{
    position:relative;
    width:950px;
    height:650px;
    border:2px solid #00f2ff;
    border-radius:15px;
    box-shadow:0 0 35px #00f2ff99;
    display:none;
    overflow:hidden;
}

/* Matrix Canvas */
#matrix{
    position:absolute;
    inset:0;
    z-index:1;
}

/* Dark overlay */
.overlay{
    position:absolute;
    inset:0;
    background:rgba(0,0,0,0.65);
    z-index:2;
}

/* UI */
.stats-display,
.action-bar,
.attack-console{
    position:relative;
    z-index:3;
}

.stats-display{
    position:absolute;
    top:120px;
    width:100%;
    display:flex;
    justify-content:center;
    gap:30px;
}

.stat-card{
    background:rgba(0,0,0,0.85);
    border:1px solid #00f2ff;
    padding:18px;
    border-radius:10px;
    min-width:160px;
    text-align:center;
    color:#00f2ff;
}

.stat-card b{
    font-size:32px;
    display:block;
    color:#0f0;
}

.action-bar{
    position:absolute;
    bottom:270px;
    width:100%;
    display:flex;
    justify-content:center;
    gap:20px;
}

.btn{
    background:rgba(0,242,255,0.1);
    border:2px solid #00f2ff;
    color:#00f2ff;
    padding:12px 45px;
    cursor:pointer;
    border-radius:6px;
    font-weight:bold;
}

.attack-console{
    position:absolute;
    bottom:35px;
    left:50%;
    transform:translateX(-50%);
    width:85%;
    height:200px;
    background:rgba(0,0,0,0.9);
    border:1px solid #00f2ff;
    padding:15px;
    overflow-y:auto;
    color:#00ffaa;
    font-size:14px;
}

.gate{
    position:fixed;
    inset:0;
    background:#000;
    z-index:999;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}

.gate input{
    background:transparent;
    border:1px solid #00f2ff;
    color:#00f2ff;
    padding:15px;
    font-size:20px;
    text-align:center;
    border-radius:6px;
}
</style>
</head>

<body>

<div class="gate" id="gate">
    <h1 style="color:#00f2ff">KAIL.911 SYSTEM</h1>
    <input id="pass" placeholder="PASSWORD">
    <br><br>
    <button class="btn" onclick="enter()">LOGIN</button>
</div>

<div class="main-container" id="mainPanel">
    <canvas id="matrix"></canvas>
    <div class="overlay"></div>

    <div class="stats-display">
        <div class="stat-card">Checked<b id="c">0</b></div>
        <div class="stat-card">Found<b id="f">0</b></div>
        <div class="stat-card">Errors<b id="e" style="color:red">0</b></div>
    </div>

    <div class="action-bar">
        <button class="btn" onclick="run('start')">START</button>
        <button class="btn" onclick="run('stop')" style="border-color:red;color:red">STOP</button>
    </div>

    <div class="attack-console" id="log-box"></div>
</div>

<script>
// ===== Matrix Effect =====
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

function resize(){
    canvas.width = document.querySelector(".main-container").clientWidth;
    canvas.height = document.querySelector(".main-container").clientHeight;
}
resize();

const letters = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%";
const fontSize = 16;
let columns = canvas.width / fontSize;
let drops = Array.from({length: columns}).fill(1);

function drawMatrix(){
    ctx.fillStyle = "rgba(0,0,0,0.08)";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle = "#00ffcc";
    ctx.font = fontSize + "px monospace";

    drops.forEach((y, i)=>{
    random()*letters.length)];
        ctx.fillText(text, i*fontSize, y*fontSize);
        if(y*fontSize > canvas.height && Math.random() > 0.975){
            drops[i]=0;
        }
        drops[i]++;
    });
}
setInterval(drawMatrix, 50);

// ===== System =====
function enter(){
    if(document.getElementById("pass").value === "hx888"){
        $("#gate").hide();
        $("#mainPanel").show();
        resize();
    } else alert("ACCESS DENIED");
}

function run(c){ $.getJSON("/cmd/"+c); }

setInterval(()=>{
    $.getJSON("/api/stats",(d)=>{
        $("#c").text(d.checked);
        $("#f").text(d.found);
        $("#e").text(d.errors);
        let h="";
        d.logs.forEach(l=>h+=`<div>[SYSTEM] ${l}</div>`);
        $("#log-box").html(h);
        document.getElementById("log-box").scrollTop=9999;
    });
},1000);
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
    if c=="start" and not hunting_active:
        hunting_active=True
        threading.Thread(target=hunt,daemon=True).start()
    if c=="stop":
        hunting_active=False
    return jsonify(ok=True)

def hunt():
    while hunting_active:
        u="".join(random.choice("abc123xyz") for _ in range(5))
        stats["checked"]+=1
        stats["logs"].append(f"Scanning @{u}")
        if len(stats["logs"])>25: stats["logs"].pop(0)
        time.sleep(0.4)

if __name__=="__main__":
    app.run("0.0.0.0",5000)

        const text = letters[Math.floor(Math.
