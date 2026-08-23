import os
import requests
from flask import Flask, request, render_template_string

# 🔑 Aapka Bot Token
TOKEN = "8979056204:AAG3LVkYw-KlPAmdlVqjM8aKMf25JKGpAqo"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

# Temporary in-memory storage
user_tasks = {}

def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    res = requests.post(URL + "sendMessage", json=payload)
    return res.json()

def edit_message(chat_id, message_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(URL + "editMessageText", json=payload)

# 🚀 Telegram Mini App ka Button (Aapka Render URL yahan set hai)
def get_tasks_keyboard():
    WEB_APP_URL = "https://mini-app-u5k2.onrender.com/webapp"
    return {
        "inline_keyboard": [
            [{"text": "🚀 Open Task Mini App", "web_app": {"url": WEB_APP_URL}}]
        ]
    }

# 🌐 Telegram Mini App ka Frontend Page
@app.route('/webapp', methods=['GET'])
def webapp():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telegram Mini App - Tasker</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: var(--tg-theme-bg-color, #ffffff);
                color: var(--tg-theme-text-color, #000000);
                padding: 20px;
                margin: 0;
            }
            .container {
                max-width: 400px;
                margin: auto;
            }
            h2 { text-align: center; }
            label { font-weight: bold; display: block; margin-top: 15px; }
            select, input, button {
                width: 100%;
                padding: 12px;
                margin-top: 5px;
                border-radius: 8px;
                border: 1px solid #ccc;
                box-sizing: border-box;
                font-size: 16px;
            }
            button {
                background-color: var(--tg-theme-button-color, #2481cc);
                color: var(--tg-theme-button-text-color, #ffffff);
                border: none;
                margin-top: 20px;
                font-weight: bold;
                cursor: pointer;
            }
            #result {
                margin-top: 20px;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🎯 Task Manager</h2>
            
            <label for="task">Select Task:</label>
            <select id="task">
                <option value="Grow">1. Grow</option>
            </select>

            <label for="tracking_url">Tracking URL:</label>
            <input type="text" id="tracking_url" placeholder="http://click.hopemobi.net/?click_id=...">

            <button onclick="submitTask()">Submit Task</button>
            <div id="result"></div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            function submitTask() {
                let task = document.getElementById('task').value;
                let url = document.getElementById('tracking_url').value;
                let userId = tg.initDataUnsafe?.user?.id || 123456;
                let resultDiv = document.getElementById('result');

                if(!url) {
                    alert("Please enter a valid tracking URL!");
                    return;
                }

                resultDiv.innerHTML = "⏳ Processing...";
                resultDiv.style.color = "orange";

                fetch('/api/process-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: userId, task: task, url: url })
                })
                .then(res => res.json())
                .then(data => {
                    if(data.success) {
                        resultDiv.innerHTML = "✅ " + data.message;
                        resultDiv.style.color = "green";
                    } else {
                        resultDiv.innerHTML = "❌ " + data.message;
                        resultDiv.style.color = "red";
                    }
                })
                .catch(err => {
                    resultDiv.innerHTML = "❌ Error connecting to server";
                    resultDiv.style.color = "red";
                });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

# 🔄 Mini App se Data Receive karne ka API Endpoint
@app.route('/api/process-task', methods=['POST'])
def process_task_api():
    data = request.get_json()
    chat_id = data.get("chat_id")
    selected_task = data.get("task", "Grow")
    text = data.get("url", "")

    # Click ID Extract karna
    click_id = "Not Found"
    if "click_id=" in text:
        try:
            click_id = text.split("click_id=")[1].split("&")[0]
        except:
            pass
    elif "clickid=" in text:
        try:
            click_id = text.split("clickid=")[1].split("&")[0]
        except:
            pass

    # Postback Request Hit Karna
    postback_url = f"http://pb.iskyworker.com/pb/lsr?transaction_id={click_id}"
    pb_status = "Failed"
    pb_response_text = ""
    task_success = False
    
    try:
        pb_res = requests.get(postback_url, timeout=10)
        pb_response_text = pb_res.text.strip()
        pb_status = f"Status {pb_res.status_code}"
        if pb_res.status_code == 200:
            task_success = True
    except Exception as e:
        pb_response_text = str(e)
        pb_status = "Connection Error"

    # Telegram chat par result message bhejna
    if task_success:
        final_text = (
            f"✅ *Mini App Task Completed*\n\n"
            f"🎯 Task: *{selected_task}*\n"
            f"🆔 Click ID: `{click_id}`\n"
            f"🟢 Postback Status: *{pb_status}*\n"
            f"📄 *PB Response:* `{pb_response_text}`"
        )
    else:
        final_text = (
            f"❌ *Mini App Task Failed*\n\n"
            f"🎯 Task: *{selected_task}*\n"
            f"🆔 Click ID: `{click_id}`\n"
            f"🔴 Postback Status: *{pb_status}*\n"
            f"📄 *Error Details:* `{pb_response_text}`"
        )
    
    send_message(chat_id, final_text)

    if task_success:
        return {"success": True, "message": "Task Completed & Postback Sent!"}
    else:
        return {"success": False, "message": f"Postback Error: {pb_status}"}

# Standard Webhook route for Telegram Bot messages
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return "Bot is active and running successfully!", 200
        
    data = request.get_json()
    if not data:
        return "OK", 200
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            welcome_text = "🚀 *Welcome to Task Bot*\n\nClick below to open the Mini App and complete your tasks easily!"
            send_message(chat_id, welcome_text, reply_markup=get_tasks_keyboard())
            
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
