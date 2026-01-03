import json, random, time, threading, asyncio, os
from flask import Flask, jsonify, request
from telegram import Bot

# --- [ إعدادات البوت ] ---
TOKEN = "6785445743:AAFQvuyfY2IIJgs2x6PnL61uA-3apHIpz2k"
ADMIN_ID = 6695916631
app = Flask(__name__)
bot = Bot(token=TOKEN)

db = {"is_running": False, "available": []}

# --- [ محرك الرادار ] ---
def radar_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        if db["is_running"]:
            target = f"user_{random.randint(100,999)}@hotmail.com"
            if random.random() > 0.95:
                hit = {"user": target, "pass": "HunteR123#"}
                db["available"].append(hit)
                try:
                    loop.run_until_complete(bot.send_message(chat_id=ADMIN_ID, text=f"🎯 صيد جديد: {target}"))
                except: pass
        time.sleep(5)

# --- [ واجهة التحكم ] ---
@app.route('/')
def index():
    return """
    <body style="background:#000; color:#0f0; font-family:monospace; text-align:center; padding-top:50px;">
        <h1 style="text-shadow: 0 0 10px #0f0;">🛰️ SYS_ACCESS: ARMY_COMMANDER_V1</h1>
        <div style="border:1px solid #0f0; display:inline-block; padding:20px; border-radius:10px; background:rgba(0,20,0,0.9);">
            <button onclick="fetch('/run?a=1')" style="background:transparent; color:#0f0; border:1px solid #0f0; padding:10px 20px; cursor:pointer;">⚡ EXECUTE_START</button>
            <button onclick="fetch('/run?a=0')" style="background:transparent; color:red; border:1px solid red; padding:10px 20px; cursor:pointer; margin-left:10px;">🛑 TERMINATE</button>
            <h2 id="logs" style="margin-top:20px;">ARMY_UNITS_ACTIVE: 0</h2>
        </div>
        <script>
            setInterval(() => {
                fetch('/status').then(r=>r.json()).then(data => {
                    document.getElementById('logs').innerHTML = "ARMY_UNITS_ACTIVE: " + data.available.length;
                });
            }, 2000);
        </script>
    </body>
    """

@app.route('/status')
def status(): return jsonify(db)

@app.route('/run')
def run():
    db["is_running"] = (request.args.get('a') == '1')
    return "ok"

if __name__ == "__main__":
    threading.Thread(target=radar_worker, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
