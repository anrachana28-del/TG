from flask import Flask, send_file, jsonify
from telethon import TelegramClient
import asyncio

# ====== Telegram API ======
api_id = 28013497
api_hash = "3bd0587beedb80c8336bdea42fc67e27"
session_name = "session.session"

# ====== Flask app ======
app = Flask(__name__)

# ====== Telethon client ======
client = TelegramClient(session_name, api_id, api_hash)

# Make sure Telethon runs before Flask
async def get_members():
    await client.start()
    members_list = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            async for user in client.iter_participants(dialog.id):
                members_list.append({
                    "name": user.first_name or "",
                    "username": user.username or "",
                    "id": user.id
                })
    return members_list

# ====== Flask routes ======
@app.route("/")
def index():
    return send_file("index.html")

@app.route("/members")
def members():
    # Run Telethon in asyncio loop
    members_list = asyncio.run(get_members())
    return jsonify(members_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
