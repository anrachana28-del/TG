import os
from telethon import TelegramClient, events
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

api_id = int(os.environ["28013497"])
api_hash = os.environ["3bd0587beedb80c8336bdea42fc67e27"]

client = TelegramClient("session", api_id, api_hash)

app = Flask(__name__, template_folder='.')  # index.html នៅ root folder
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route("/")
def index():
    return render_template("index.html")

@client.on(events.NewMessage(incoming=True))
async def on_message(event):
    chat = await event.get_chat()
    data = {
        "chat_id": event.chat_id,
        "name": getattr(chat, "title", None) or chat.first_name,
        "username": getattr(chat, "username", None),
        "text": event.text
    }
    socketio.emit("telegram_message", data)

@socketio.on("send_message")
def send_message(data):
    chat_id = data.get("chat_id")
    text = data.get("text")
    if chat_id and text:
        client.loop.create_task(client.send_message(chat_id, text))

if __name__ == "__main__":
    client.start()
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
