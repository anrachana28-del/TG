import os
from telethon import TelegramClient, events
from flask import Flask
from flask_socketio import SocketIO

api_id = int(os.environ["28013497"])
api_hash = os.environ["3bd0587beedb80c8336bdea42fc67e27"]

client = TelegramClient("session", api_id, api_hash)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")


@client.on(events.NewMessage(incoming=True))
async def handler(event):
    chat = await event.get_chat()
    socketio.emit("telegram_message", {
        "chat_id": event.chat_id,
        "name": getattr(chat, "title", None) or chat.first_name,
        "text": event.text
    })


if __name__ == "__main__":
    client.start()
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
