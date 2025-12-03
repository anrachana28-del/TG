import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from flask import Flask, render_template
from flask_socketio import SocketIO

api_id = 28013497
api_hash = "3bd0587beedb80c8336bdea42fc67e27"
session_name = "session"  # session.session

# Flask setup
app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Telethon setup
client = TelegramClient(session_name, api_id, api_hash)

async def get_members():
    await client.start()  # uses session.session
    # Replace with your target chat/group username or ID
    target = "https://t.me/YOUR_GROUP_OR_CHANNEL"
    members = []
    async for user in client.iter_participants(target):
        members.append({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
    return members

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    async def send_members():
        members = await get_members()
        socketio.emit("members", members)
    asyncio.run(send_members())

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
