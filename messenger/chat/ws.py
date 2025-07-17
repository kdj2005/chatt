from manager.manager import manager
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
from database import db
from .logique import save_message
from model import message_dict
from bson import ObjectId
from typing import Dict, List
import json


#la fonction qui gerene les messages privés
async def private_chat_ws(websocket: WebSocket, sender: str, receiver: str):
    await manager.connect(websocket, sender)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)

                if isinstance(msg, dict):
                    if msg.get("type") == "audio":
                        await save_message(sender, receiver, "", msg_type="audio", audio_data=msg["data"])
                        msg_obj = {
                            "sender": sender,
                            "audio": msg["data"],
                            "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "type": "audio"
                        }
                    elif msg.get("type", "").startswith("call_"):
                        # Relais du signal d'appel à l'autre utilisateur
                        await manager.send_private_message(msg, receiver, sender)
                        continue
                    elif msg.get("type") == "image":
                        await save_message(sender, receiver, "", msg_type="image", image_data=msg["data"])
                        msg_obj = {
                            "sender": sender,
                            "image": msg["data"],
                            "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "type": "image"
                        }
                    elif msg.get("type") == "video":
                        await save_message(sender, receiver, "", msg_type="video", video_data=msg["data"])
                        msg_obj = {
                            "sender": sender,
                            "video": msg["data"],
                            "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "type": "video"
                        }
                    elif msg.get("type") == "file":
                        await save_message(sender, receiver, "", msg_type="file", file_data=msg["data"])
                        msg_obj = {
                            "sender": sender,
                            "file": msg["data"],
                            "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "type": "file"
                        }
                    elif msg.get("type") == "typing":
                        await manager.broadcast_typing(sender, receiver, msg["typing"])
                        continue
                    elif msg.get("type") == "seen":
                        # Marquer le message comme lu côté DB
                        from .logique import mark_message_seen
                        message_id = msg.get("message_id")
                        if message_id:
                            await mark_message_seen(message_id)
                        msg_obj = {
                            "type": "seen",
                            "from": sender,
                            "message_id": message_id,
                            "message": "Message vu"
                        }
                        await manager.send_private_message(msg_obj, receiver, sender)
                        continue
                    else:
                        message = msg.get("message", "")
                        await save_message(sender, receiver, message)
                        msg_obj = {
                            "sender": sender,
                            "message": message,
                            "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "type": "text"
                        }
                else:
                    await save_message(sender, receiver, data)
                    msg_obj = {
                        "sender": sender,
                        "message": data,
                        "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "type": "text"
                    }

                print(f"Envoi message : sender={sender!r}, receiver={receiver!r}, msg_obj={msg_obj}")
                try:
                    await manager.send_private_message(msg_obj, receiver, sender)
                except Exception as ex:
                    print("Erreur lors de l'envoi WebSocket :", ex)
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
    except WebSocketDisconnect:
        manager.disconnect(sender)