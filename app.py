from flask import Flask, render_template_string, jsonify
import threading, time, random

app = Flask(__name__)

# إعدادات النظام
PASSWORD_ACCESS = "hx5"
ADMIN_NAME = "Mohamed Security"
USER_TAG = "kail.911"

is_running = False
results_list = []

def hacking_engine():
    global is_running, results_list
    while is_running:
        new_entry = {
            "time": time.strftime("%H:%M:%S"),
            "target": "ID_" + str(random.randint(1000, 9999)),
            "status": "RUNNING 📡"
        }
        results_list.insert(0, new_entry)
        if len(results_list) > 15: results_list.pop()
        time.sleep(2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }}</title>
    <style>
        :root { --main: #00ff41; }
        body { background: #000; color: var(--main); font-family: 'Courier New', monospace; margin: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; }
        canvas { position: absolute; top: 0; left: 0; z-index: -1; }
        .box { background: rgba(0, 10, 0, 0.9); border: 1px solid var(--main); padding: 40px; border-radius: 15px; box-shadow: 0 0 25px var(--main); text-align: center; width: 90%; max-width: 500px; z-index: 10; }
        input { background: transparent; border: 1px solid var(--main); color: #fff; padding: 15px; width: 80%; margin: 20px 0; text-align: center; font-size: 1.2em; border-radius: 5px; outline: none; }
        button { background: var(--main); color: #000; border: none; padding: 12px 30px; cursor: pointer; font-weight: bold; border-radius: 5px; text-transform: uppercase; margin: 10px; }
        .hidden { display: none !important; }
        table { width: 100%; margin-top: 20px; border-collapse: collapse; }
        th, td { border: 1px solid var(--main); padding: 10px; font-size: 0.8em; }
        .tag { color: #fff; background: rgba(0,255,65,0.2); padding: 5px 10px; border-radius: 20px; font-size: 0.9em; }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>

    <div id="login_ui" class="box">
        <h1 style="text-shadow: 0 0 10px var(--main);">{{ name }}</h1>
        <span class="tag">@{{ tag }}</span>
        <input type="password" id="key" placeholder="ACCESS CODE">
        <br>
        <button onclick="access()">BOOT SYSTEM</button>
    </div>

    <div id="dash_ui" class="box hidden">
        <h1 style="font-size: 1.5em;">DASHBOARD ACTIVE</h1>
        <button onclick="start()" style="background: #28a745; color: white;">START ENGINE</button>
        <button onclick="location.reload()" style="background: #ff4444; color: white;">TERMINATE</button>
        <table>
            <thead><tr><th>TIME</th><th>MISSION</th><th>STATUS</th></tr></thead>
            <tbody id="logs"></tbody>
        </table>
    </div>

    <script>
        // Matrix Animation
        const c = document.getElementById('canvas');
        const ctx = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        const drops = Array(Math.floor(c.width/16)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,c.width,c.height);
            ctx.fillStyle = "#0f0"; ctx.font = "15px arial";
            drops.forEach((y, i) => {
                ctx.fillText(Math.floor(Math.random()*2), i*16, y*16);
                if(y*16 > c.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 33);

        // Access Logic
        function access() {
            const inputKey = document.getElementById('key').value;
            if(inputKey === "{{ pw }}") {
                document.getElementById('login_ui').classList.add('hidden');
                document.getElementById('dash_ui').classList.remove('hidden');
                setInterval(updateLogs, 2000);
            } else {
                alert("INVALID KEY!");
            }
        }

        function start() { fetch('/api/start'); }
       function updateLogs() {
            fetch('/api/logs').then(r => r.json()).then(data => {
                let rows = '';
                data.forEach(item => {
                    rows += <tr><td>${item.time}</td><td>${item.target}</td><td>${item.status}</td></tr>;
                });
                document.getElementById('logs').innerHTML = rows;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, name=ADMIN_NAME, tag=USER_TAG, pw=PASSWORD_ACCESS)

@app.route('/api/start')
def start_engine():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=hacking_engine, daemon=True).start()
    return jsonify(s="ok")

@app.route('/api/logs')
def get_logs():
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 
