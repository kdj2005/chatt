from fastapi import Request,HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from model import group_dict, notification_dict,message_dict
from database import db
from manager.manager import manager
from datetime import datetime
from typing import Dict
import json





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

#fonction qui permet de creer un groupe de discussion
async def create_group(request: Request):
    data = await request.json()
    name = data.get("name")
    creator = data.get("creator")
    members = data.get("members", [])
    if not name or not creator or not members:
        return JSONResponse({"success": False, "error": "Paramètres manquants"})
    group = group_dict(name, creator, members)
    result = await db.groups.insert_one(group)
    group_id = str(result.inserted_id)
    # Notifier les membres (sauf le créateur)
    for user_id in members:
        if user_id != creator:
            notif = notification_dict(user_id, "group_add", group=name)
            await db.notifications.insert_one(notif)
    return JSONResponse({"success": True, "group_id": group_id})

#fonction qui permet de listés  les groupes d'un utilisateur
async def user_groups(user_id: str):
    groups = db.groups.find({"members": user_id})
    result = []
    async for group in groups:
        result.append({
            "id": str(group["_id"]),
            "name": group["name"],
            "memberCount": len(group["members"])
        })
    return {"groups": result}

#la fonction qui permet de retrouver un groupe par son ID
async def get_group_members(group_id: str):
    group = await db.groups.find_one({"_id": ObjectId(group_id)})
    if not group:
        raise HTTPException(status_code=404, detail="Groupe introuvable")
    return {"members": group["members"], "creator": group["creator"]}

#la fonction qui permet d'ajouter un membre a un groupe
async def add_member(group_id: str, request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    actor = data.get("actor") 
    group = await db.groups.find_one({"_id": ObjectId(group_id)})
    if not group or not user_id or not actor:
        raise HTTPException(status_code=404, detail="Groupe ou utilisateur introuvable")
    if actor != group["creator"]:
        raise HTTPException(status_code=403, detail="Seul le créateur peut ajouter des membres")
    if user_id not in group["members"]:
        await db.groups.update_one({"_id": ObjectId(group_id)}, {"$push": {"members": user_id}})
        notif = notification_dict(user_id, "group_add", group=group["name"])
        await db.notifications.insert_one(notif)
    return {"success": True}

#la fonction qui permet de retirer un membre d'un groupe
async def remove_member(group_id: str, request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    actor = data.get("actor")
    group = await db.groups.find_one({"_id": ObjectId(group_id)})
    print("actor:", actor, "creator:", group["creator"])
    if not group or not user_id:
        raise HTTPException(status_code=404, detail="Groupe ou utilisateur introuvable")
    if actor != group["creator"]:
        raise HTTPException(status_code=403, detail="Seul le créateur peut retirer des membres")
    if user_id in group["members"]:
        await db.groups.update_one({"_id": ObjectId(group_id)}, {"$pull": {"members": user_id}})
        notif = notification_dict(user_id, "group_remove", group=group["name"])
        await db.notifications.insert_one(notif)
    return {"success": True}

#la fonction qui permet d'avoir les message d'un groupe
async def get_group_messages(group_id: str):
    messages = db.messages.find({"group_id": ObjectId(group_id)}).sort("created_at", 1)
    result = []
    async for msg in messages:
        result.append(serialize_message(msg))
    return {"messages": result}



