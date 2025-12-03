from telethon import TelegramClient

api_id = 28013497
api_hash = "3bd0587beedb80c8336bdea42fc67e27"
session_name = "session.session"

client = TelegramClient(session_name, api_id, api_hash)

async def fetch_messages(group_id, limit=50):
    messages_list = []
    async for msg in client.iter_messages(group_id, limit=limit):
        messages_list.append({
            "id": msg.id,
            "sender_id": msg.sender_id,
            "text": msg.text,
            "date": str(msg.date)
        })
    return messages_list

async def fetch_members(group_id):
    members_list = []
    async for user in client.iter_participants(group_id):
        members_list.append({
            "id": user.id,
            "name": user.first_name or "",
            "username": user.username or ""
        })
    return members_list
