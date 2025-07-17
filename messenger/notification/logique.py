from fastapi import HTTPException
from bson import ObjectId
from database import db





#supprimer une notication
async def delete_notification(notif_id: str):
    
    await db.notifications.delete_one({"_id": ObjectId(notif_id)})
    return {"success": True}

#la fonction qui permet de  marquer une notification comme lue
async def mark_notifications_read(user_id: str):
    await db.notifications.update_many({"user_id": user_id, "read": False}, {"$set": {"read": True}})
    return {"success": True}

# Récupérer les notifications non lues d'un utilisateur
async def get_notifications(user_id: str):
    notifs = db.notifications.find({"user_id": user_id, "read": False})
    result = []
    async for notif in notifs:
        notif["_id"] = str(notif["_id"])
        result.append(notif)
    return {"notifications": result}
