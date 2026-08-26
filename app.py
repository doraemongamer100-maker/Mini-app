import os
import time
import threading
import requests
from urllib.parse import urlparse, parse_qs, unquote
from flask import Flask, request, render_template_string

TOKEN = "8874819641:AAG_da4XGX2CoTsLiQgyV3QKCcC_OOYxJIs"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# Force Channel Join Settings
CHANNEL_USERNAME = "@Dragon_Scripterr"
CHANNEL_URL = "https://t.me/Dragon_Scripterr"

app = Flask(__name__)
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

def check_user_subscription(chat_id):
    try:
        res = requests.get(f"{URL}getChatMember", params={"chat_id": CHANNEL_USERNAME, "user_id": chat_id})
        data = res.json()
        if data.get("ok"):
            status = data["result"].get("status")
            if status in ["member", "administrator", "creator"]:
                return True
    except Exception:
        pass
    return False

def get_join_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "📢 Join Channel", "url": CHANNEL_URL}],
            [{"text": "🔄 Check Membership", "callback_data": "check_subscription"}]
        ]
    }

# 🚀 Mini App Web App Button (Updated Render URL)
def get_webapp_keyboard():
    WEB_APP_URL = "https://mini-appp-0may.onrender.com/"
    return {
        "inline_keyboard": [
            [{"text": "🚀 Open Task Mini App", "web_app": {"url": WEB_APP_URL}}]
        ]
    }

# 🌐 Telegram Mini App HTML/JS UI Route
@app.route('/', methods=['GET'])
def webapp():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Manager Mini App</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: var(--tg-theme-bg-color, #0f172a);
                color: var(--tg-theme-text-color, #f8fafc);
                padding: 15px;
                margin: 0;
            }
            .container {
                max-width: 450px;
                margin: auto;
            }
            h2 { text-align: center; color: #38bdf8; margin-bottom: 5px; }
            p.subtitle { text-align: center; font-size: 13px; color: #94a3b8; margin-top: 0; }
            label { font-weight: bold; display: block; margin-top: 15px; font-size: 14px; }
            select, input, button {
                width: 100%;
                padding: 12px;
                margin-top: 6px;
                border-radius: 8px;
                border: 1px solid #334155;
                box-sizing: border-box;
                font-size: 15px;
                background-color: #1e293b;
                color: #f8fafc;
            }
            select:focus, input:focus {
                border-color: #38bdf8;
                outline: none;
            }
            button {
                background-color: #0284c7;
                color: #ffffff;
                border: none;
                margin-top: 22px;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.2s;
            }
            button:hover { background-color: #0369a1; }
            #result {
                margin-top: 20px;
                padding: 12px;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                font-size: 14px;
                word-break: break-all;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🎯 Task Manager</h2>
            <p class="subtitle">Select your task and paste tracking URL</p>
            
            <label for="task">Select Task:</label>
            <select id="task">
                <option value="Grow">1. Grow</option>
                <option value="Solitaire">2. Solitaire</option>
                <option value="Policy Bazaar">3. Policy Bazaar</option>
                <option value="Condivio">4. Condivio</option>
                <option value="Uni">5. Uni</option>
                <option value="Amazon">6. Amazon</option>
                <option value="Vivago">7. Vivago</option>
                <option value="Rapid Rupee">8. Rapid Rupee</option>
                <option value="Novio">9. Novio</option>
                <option value="Aspro Bonds">10. Aspro Bonds</option>
                <option value="Truemads">11. Truemads</option>
                <option value="Incred">12. Incred</option>
                <option value="Candy Crush">13. Candy Crush</option>
            </select>

            <label for="tracking_url">Tracking URL:</label>
            <input type="text" id="tracking_url" placeholder="Paste your tracking URL here...">

            <button onclick="submitTask()">🚀 Submit & Process Task</button>
            <div id="result"></div>
        </div>

        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();

            function submitTask() {
                let task = document.getElementById('task').value;
                let url = document.getElementById('tracking_url').value;
                let userId = tg.initDataUnsafe?.user?.id;
                let resultDiv = document.getElementById('result');

                if (!userId) {
                    userId = 123456; 
                }

                if(!url) {
                    alert("Please enter a valid tracking URL!");
                    return;
                }

                resultDiv.innerHTML = "⏳ Processing task, please wait...";
                resultDiv.style.color = "#fbbf24";
                resultDiv.style.background = "#334155";

                fetch('/api/process-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: userId, task: task, url: url })
                })
                .then(res => res.json())
                .then(data => {
                    if(data.success) {
                        resultDiv.innerHTML = "✅ " + data.message + "<br><small>Check your Telegram bot chat for detailed logs!</small>";
                        resultDiv.style.color = "#4ade80";
                        resultDiv.style.background = "#064e3b";
                    } else {
                        resultDiv.innerHTML = "❌ " + data.message;
                        resultDiv.style.color = "#f87171";
                        resultDiv.style.background = "#7f1d1d";
                    }
                })
                .catch(err => {
                    resultDiv.innerHTML = "❌ Error connecting to server.";
                    resultDiv.style.color = "#f87171";
                    resultDiv.style.background = "#7f1d1d";
                });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

# Background processing function for Vivago
def process_vivago_events(chat_id, text):
    try:
        parsed_url = urlparse(text)
        query_params = parse_qs(parsed_url.query)
        
        click_id = "Not Found"
        events = []
        
        for key, values in query_params.items():
            val = values[0]
            if "mobvista_clickid" in val or "clickid" in key.lower():
                if "mobvista_clickid=" in val:
                    sub_params = parse_qs(val.replace('&', ';'))
                    if "mobvista_clickid" in sub_params:
                        click_id = sub_params["mobvista_clickid"][0]
                elif "clickid=" in val:
                    try:
                        click_id = val.split("clickid=")[1].split("&")[0]
                    except:
                        pass
                        
        if click_id == "Not Found":
            if "mobvista_clickid=" in text:
                try:
                    click_id = text.split("mobvista_clickid=")[1].split("&")[0]
                except:
                    pass
            elif "clickid=" in text:
                try:
                    click_id = text.split("clickid=")[1].split("&")[0]
                except:
                    pass

        for key, values in query_params.items():
            if key.startswith("event_callback_") or "install_callback" in key:
                decoded_val = unquote(values[0])
                while "%" in decoded_val:
                    decoded_val = unquote(decoded_val)
                    
                if "event_name=" in decoded_val:
                    try:
                        e_name = decoded_val.split("event_name=")[1].split("&")[0]
                        if e_name and e_name not in events:
                            events.append(e_name)
                    except:
                        pass
                elif "install_callback" in key or "mobvista_install" in decoded_val:
                    if "install" not in events:
                        events.append("install")

        if not events:
            events = ["install", "sign_up", "iap_purchase", "session"]

        init_msg = send_message(chat_id, f"🚀 *Processing Vivago Task...*\n\n🆔 Click ID: `{click_id}`\n📋 Total Events Found: `{len(events)}`\n⏳ *Sending events with 5s delay each...*")
        
        results_log = []
        success_count = 0
        
        for index, ev in enumerate(events):
            if index > 0:
                if init_msg and "result" in init_msg:
                    msg_id = init_msg["result"]["message_id"]
                    for remaining in range(5, 0, -1):
                        edit_message(chat_id, msg_id, f"🚀 *Processing Vivago Task...*\n\n🆔 Click ID: `{click_id}`\n⏳ *Waiting {remaining}s before next event ({ev})...*")
                        time.sleep(1)
                else:
                    time.sleep(5)
                
            pb_url = f"http://stat.advcorp.net/event?clickid={click_id}&event_name={ev}"
            try:
                res = requests.get(pb_url, timeout=10)
                if res.status_code == 200:
                    success_count += 1
                    results_log.append(f"✅ `{ev}`: Success")
                else:
                    results_log.append(f"❌ `{ev}`: Failed")
            except Exception as e:
                results_log.append(f"❌ `{ev}`: Error")

        logs_str = "\n".join(results_log)
        status_heading = "✅ *Task Bypass Successful*" if success_count > 0 else "❌ *Failed*"
        final_text = (
            f"{status_heading}\n\n"
            f"🎯 Task: *Vivago*\n"
            f"🆔 Click ID: `{click_id}`\n"
            f"📊 Successful Hits: `{success_count}/{len(events)}`\n\n"
            f"📄 *Details:*\n{logs_str}"
        )
        
        if init_msg and "result" in init_msg:
            msg_id = init_msg["result"]["message_id"]
            edit_message(chat_id, msg_id, final_text)
        else:
            send_message(chat_id, final_text)
            
    except Exception as ex:
        send_message(chat_id, f"❌ *Error processing Vivago URL:* `{str(ex)}`")

# Background processing function for other tasks
def process_standard_task(chat_id, selected_task, text):
    click_id = "Not Found"
    postback_url = ""

    if selected_task == "Grow":
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
        postback_url = f"http://pb.iskyworker.com/pb/lsr?transaction_id={click_id}"

    elif selected_task in ["Solitaire", "Policy Bazaar", "Amazon", "Rapid Rupee", "Novio", "Candy Crush"]:
        if "clickid=" in text:
            try:
                click_id = text.split("clickid=")[1].split("&")[0]
            except:
                pass
        elif "label=" in text:
            try:
                click_id = text.split("label=")[1].split("&")[0]
            except:
                pass
        elif "p1=" in text:
            try:
                click_id = text.split("p1=")[1].split("&")[0]
            except:
                pass
        postback_url = f"http://postback.milengine.com/?adv=1000444&clickid={click_id}"

    elif selected_task in ["Condivio", "Uni", "Aspro Bonds", "Truemads", "Incred"]:
        if "clickid=" in text:
            try:
                click_id = text.split("clickid=")[1].split("&")[0]
            except:
                pass
        elif "click_id=" in text:
            try:
                click_id = text.split("click_id=")[1].split("&")[0]
            except:
                pass
        elif "p1=" in text:
            try:
                click_id = text.split("p1=")[1].split("&")[0]
            except:
                pass
        postback_url = f"http://pb.imxbidding.net/pb/lsr?transaction_id={click_id}"

    init_msg = send_message(chat_id, f"🚀 *Processing Task...*\n\n🎯 Task: *{selected_task}*\n🆔 Click ID: `{click_id}`\n⏳ *Waiting 5 seconds before hitting postback...*")
    
    if init_msg and "result" in init_msg:
        msg_id = init_msg["result"]["message_id"]
        for remaining in range(5, 0, -1):
            edit_message(chat_id, msg_id, f"🚀 *Processing Task...*\n\n🎯 Task: *{selected_task}*\n🆔 Click ID: `{click_id}`\n⏳ *Waiting {remaining} seconds...*")
            time.sleep(1)
    else:
        time.sleep(5)

    pb_status = "Failed"
    pb_response_text = ""
    task_success = False
    
    try:
        pb_res = requests.get(postback_url, timeout=10)
        raw_response = pb_res.text.strip()
        pb_status = f"Status {pb_res.status_code}"
        
        if "http://" in raw_response or "https://" in raw_response:
            pb_response_text = "Success (URL hidden)"
        else:
            pb_response_text = raw_response

        if pb_res.status_code == 200:
            task_success = True
    except Exception as e:
        pb_response_text = "Connection Error"
        pb_status = "Connection Error"

    if task_success:
        final_text = (
            f"✅ *Task Bypass Successful*\n\n"
            f"🎯 Task: *{selected_task}*\n"
            f"🆔 Click ID: `{click_id}`\n"
            f"🟢 Postback Status: *{pb_status}*\n"
            f"📄 *PB Response:* `{pb_response_text}`"
        )
    else:
        final_text = (
            f"❌ *Failed*\n\n"
            f"🎯 Task: *{selected_task}*\n"
            f"🆔 Click ID: `{click_id}`\n"
            f"🔴 Postback Status: *{pb_status}*\n"
            f"📄 *Error Details:* `{pb_response_text}`"
        )
    
    if init_msg and "result" in init_msg:
        msg_id = init_msg["result"]["message_id"]
        edit_message(chat_id, msg_id, final_text)
    else:
        send_message(chat_id, final_text)

# API Endpoint for Mini App Task Submission
@app.route('/api/process-task', methods=['POST'])
def process_task_api():
    data = request.get_json()
    if not data:
        return {"success": False, "message": "No data received"}, 400
        
    chat_id = data.get("chat_id")
    selected_task = data.get("task", "Grow")
    text = data.get("url", "")

    if not chat_id or not text:
        return {"success": False, "message": "Invalid parameters"}, 400

    if not check_user_subscription(chat_id):
        return {"success": False, "message": "Access Denied! Please join our channel first."}, 403

    if selected_task == "Vivago":
        threading.Thread(target=process_vivago_events, args=(chat_id, text)).start()
    else:
        threading.Thread(target=process_standard_task, args=(chat_id, selected_task, text)).start()

    return {"success": True, "message": f"Task '{selected_task}' submitted successfully!"}

# Telegram Bot Webhook Route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return "OK", 200
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if not check_user_subscription(chat_id):
            send_message(chat_id, "⚠️ *Access Denied!*\n\nYou must join our channel first to use this bot.", reply_markup=get_join_keyboard())
            return "OK", 200
        
        if text == "/start":
            welcome_text = "🚀 *Welcome to Task Bot*\n\nClick below to open the Mini App and complete your tasks easily!"
            send_message(chat_id, welcome_text, reply_markup=get_webapp_keyboard())
            
    elif "callback_query" in data:
        cq = data["callback_query"]
        chat_id = cq["message"]["chat"]["id"]
        message_id = cq["message"]["message_id"]
        query_id = cq["id"]
        data_str = cq["data"]
        
        requests.post(URL + "answerCallbackQuery", json={"callback_query_id": query_id})
        
        if data_str == "check_subscription":
            if check_user_subscription(chat_id):
                welcome_text = "🚀 *Welcome*\n\nClick below to open the Mini App:"
                edit_message(chat_id, message_id, welcome_text, reply_markup=get_webapp_keyboard())
            else:
                requests.post(URL + "answerCallbackQuery", json={
                    "callback_query_id": query_id,
                    "text": "❌ You haven't joined the channel yet!",
                    "show_alert": True
                })
            return "OK", 200

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
                                                      
