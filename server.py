from flask import Flask, render_template, jsonify
from telethon import TelegramClient

# Telegram API
api_id = 28013497
api_hash = "3bd0587beedb80c8336bdea42fc67e27"
session_name = "session"  # session.session file

# Flask app
app = Flask(__name__)

# Telegram client
client = TelegramClient(session_name, api_id, api_hash)
client.start()  # Will use uploaded session.session automatically

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/members/<int:chat_id>")
async def get_members(chat_id):
    # Get participants
    participants = await client.get_participants(chat_id)
    data = []
    for user in participants:
        data.append({
            "id": user.id,
            "first_name": getattr(user, "first_name", ""),
            "last_name": getattr(user, "last_name", ""),
            "username": getattr(user, "username", ""),
            "phone": getattr(user, "phone", "")
        })
    return jsonify(data)

if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()  # allow Flask + asyncio
    app.run(host="0.0.0.0", port=5000, debug=True)
