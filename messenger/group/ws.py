from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from manager.manager import manager
from model import message_dict
from database import db
import json
from typing import Dict, List
from datetime import datetime
from bson import ObjectId

#la fonction d'envoie de message dans un groupe via websocket
async def group_chat(websocket: WebSocket, group_id: str, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                msg_type = msg.get("type", "text")
                message = msg.get("message", "")
                audio = msg.get("audio") or msg.get("data")
                image = msg.get("image") or msg.get("data")
                video = msg.get("video") or msg.get("data")
                file = msg.get("file") or msg.get("data")
                # Enregistre le message en base
                msg_db = message_dict(
                    room_id=None,
                    sender=username,
                    msg_type=msg_type,
                    message=message,
                    audio_data=audio,
                    group_id=ObjectId(group_id),
                    file_data=file,
                    image_data=image,
                    video_data=video
                )
                await db.messages.insert_one(msg_db)
                # Prépare l'objet à envoyer aux membres
                msg_obj = {
                    "sender": username,
                    "message": message,
                    "audio": audio,
                    "image": image,
                    "video": video,
                    "file": file,
                    "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "type": msg_type
                }
                # Broadcast à tous les membres connectés du groupe
                group = await db.groups.find_one({"_id": ObjectId(group_id)})
                if group:
                    for member in group["members"]:
                        ws = manager.active_connections.get(member)
                        if ws:
                            await ws.send_text(json.dumps(msg_obj))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
    except WebSocketDisconnect:
        manager.disconnect(username)
