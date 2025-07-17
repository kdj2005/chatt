from fastapi import APIRouter, WebSocket, Request
from .logique import get_messages
from fastapi.responses import JSONResponse
from manager.manager import manager
from .ws import private_chat_ws
router = APIRouter()

#la route pour recueillir les messages
@router.get("/messages/{user1}/{user2}")
async def getmessages(user1: str, user2: str):
    return await get_messages(user1, user2)



#la route pour envoyer un message privé
@router.websocket("/ws/private/{sender}/{receiver}")
async def private_chat(websocket: WebSocket, sender: str, receiver: str):
    return await private_chat_ws(websocket, sender, receiver)




@router.get("/users")
async def get_users():
   return JSONResponse(manager.get_users())