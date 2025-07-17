from model import room_dict, message_dict, group_dict, notification_dict
from database import db
from bson import ObjectId
from datetime import datetime
from typing import Dict



#fonction pour creer une salle de discussion entre deux utilisateurs
async def get_or_create_room(user1: str, user2: str):
    members = sorted([user1, user2])
    room = await db.rooms.find_one({"members": members})
    if not room:
        result = await db.rooms.insert_one(room_dict(user1, user2))
        room = await db.rooms.find_one({"_id": result.inserted_id})
    return room

#fonction pour sauvegarder  les messages d'une conversation dans la db
async def save_message(sender: str, receiver: str, message: str, msg_type="text", audio_data=None, seen=False, file_data=None, image_data=None, video_data=None):
    room = await get_or_create_room(sender, receiver)
    msg = message_dict(room["_id"], sender, msg_type=msg_type, message=message, audio_data=audio_data, seen=seen, file_data=file_data, image_data=image_data, video_data=video_data)
    await db.messages.insert_one(msg)

# Fonction pour recuperer les messages d'une salle de discussion

async def get_room_messages(user1: str, user2: str):
    room = await get_or_create_room(user1, user2)
    messages = db.messages.find({"room_id": room["_id"]}).sort("created_at", 1)
    return [msg async for msg in messages]

# Fonction pour serialiser un message pour l'envoi au client
def serialize_message(msg):
    msg = dict(msg)
    # Conversion ObjectId -> str pour tous les champs concernés
    for key in ["_id", "room_id", "group_id"]:
        if key in msg and isinstance(msg[key], ObjectId):
            msg[key] = str(msg[key])
    if "created_at" in msg and isinstance(msg["created_at"], datetime):
        msg["time"] = msg["created_at"].strftime("%d/%m/%Y %H:%M")
    elif "createdAt" in msg and isinstance(msg["createdAt"], datetime):
        msg["time"] = msg["createdAt"].strftime("%d/%m/%Y %H:%M")
    return msg

# Fonction pour recuperer les messages d'une conversation
async def get_messages(user1: str, user2: str):
    messages = await get_room_messages(user1, user2)
    messages = [serialize_message(msg) for msg in messages]
    return {"messages": messages}


# Fonction pour marquer un message comme lu (seen)
async def mark_message_seen(message_id: str):
    from bson import ObjectId
    result = await db.messages.update_one({"_id": ObjectId(message_id)}, {"$set": {"seen": True}})
    return result.modified_count > 0





