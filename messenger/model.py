from datetime import datetime
from bson import ObjectId

def user_dict(email: str, password_hash: str, pseudo: str = ""):
    return {
        "email": email,
        "password_hash": password_hash,
        "pseudo": pseudo,
        "created_at": datetime.utcnow(),
        "otp": None, 
    }

def message_dict(room_id: ObjectId, sender: str, msg_type="text", message: str = "", audio_data=None, seen: bool = False, group_id: ObjectId = None, file_data=None, image_data=None, video_data=None):
    # Peut servir pour message privé (room_id) ou groupe (group_id)
    return {
        "room_id": room_id,
        "group_id": group_id,
        "sender": sender,
        "type": msg_type,
        "message": message,
        "audio": audio_data,
        "file": file_data,
        "image": image_data,
        "video": video_data,
        "created_at": datetime.utcnow(),
        "seen": seen
    }

def room_dict(user1: str, user2: str):
    return {
        "members": sorted([user1, user2]),
        "created_at": datetime.utcnow()
    }

def group_dict(name: str, creator: str, members: list):
    return {
        "name": name,
        "creator": creator,
        "members": list(set(members + [creator])),
        "created_at": datetime.utcnow()
    }

def notification_dict(user_id: str, notif_type: str, group: str = "", read: bool = False):
    return {
        "user_id": user_id,
        "type": notif_type,  # "group_add" ou "group_remove"
        "group": group,
        "created_at": datetime.utcnow(),
        "read": read
    }