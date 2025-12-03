from telethon import TelegramClient, events
from flask import Flask
from flask_socketio import SocketIO

api_id = 28013497
api_hash = "3bd0587beedb80c8336bdea42fc67e27"

client = TelegramClient("session", api_id, api_hash)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


# ✅ ទទួលសារពី Telegram account ផ្ទាល់
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


if __name__ == "__main__":
    client.start()
    socketio.run(app, host="0.0.0.0", port=5000)
