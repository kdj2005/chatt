from fastapi import APIRouter
from .logique import delete_notification, mark_notifications_read, get_notifications

router = APIRouter()

@router.get("/notification-get/{user_id}")
async def notifications(user_id: str):
    return await get_notifications(user_id)

@router.post("/notification-read/{user_id}")
async def mark_read(user_id: str):
    return await mark_notifications_read(user_id)

@router.delete("/notification-delete/{notif_id}")
async def delete(notif_id: str):
    return await delete_notification(notif_id)