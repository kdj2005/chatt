from fastapi import APIRouter,Request,HTTPException,WebSocket
from .logique import create_group,user_groups,get_group_members,add_member,remove_member,get_group_messages
from .ws import group_chat

router=APIRouter()


#la route pour creer un groupe
@router.post("/create-group")
async def creer_group(request: Request):
    return await create_group(request)


#  route pour Liste des groupes d'un utilisateur
@router.get("/user-groups/{user_id}")
async def group_of_user(user_id: str):
  return await user_groups(user_id)

#  route  pour Membres d'un groupe
@router.get("/group-members/{group_id}")
async def group_members(group_id: str):
    return await get_group_members(group_id)
   

#  route pour ajouter un membre à un groupe
@router.post("/group/{group_id}/add-member")
async def ajout_member(group_id: str, request: Request):
    return await add_member(group_id,request)
 
# route pour retirer un membre d'un groupe
@router.delete("/group/{group_id}/remove-member")
async def retrait_member(group_id: str, request: Request):
   return await remove_member(group_id, request)

# route pour  recuperer les  Messages de groupe
@router.get("/group-messages/{group_id}")
async def group_messages(group_id: str):
    return await get_group_messages(group_id)

#  route pour envoi message de groupe (via WebSocket)
@router.websocket("/ws/group/{group_id}/{username}")
async def chat_group(websocket: WebSocket, group_id: str, username: str):
        return await group_chat(websocket, group_id, username)  
   