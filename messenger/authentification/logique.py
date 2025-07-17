from fastapi.responses import JSONResponse
from fastapi import Request
from model import user_dict
from database import db
from manager.manager import manager
from .utils import send_bienvenue,send_otp,generate_otp,authenticate_user,create_user,hash_password


#la fonction qui permet a l'utilisateur de creer un compte pour la premiere fois
async def register_user(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    pseudo = data.get("pseudo", "")
    success = await create_user(email, password, pseudo)
    if success:
        await send_bienvenue(email, pseudo)

    return JSONResponse({"success": success})
#la fonction qui permet a l'utilisateur de se connecter
async def login_user(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    is_valid = await authenticate_user(email, password)
    pseudo = None
    if is_valid:
        user = await db.users.find_one({"email": email})
        if user:
            pseudo = user.get("pseudo")
            manager.register(pseudo)
    return JSONResponse({"success": is_valid, "pseudo": pseudo if is_valid else None})

#la fonction qui verify l'email de l'utilsateur et lui envoie un code de verification
async def verify_email(request:Request):
    data=await request.json()
    email=data.get("email")
    user=await db.users.find_one({"email": email})
    if user:
        otp=generate_otp()
        await db.users.update_one({"email": email}, {"$set": {"otp": otp}})
        await send_otp(email, otp)
        return  JSONResponse({"success":True,"message":"L'email est valide et un OTP a été envoyé"})

    else:
        return JSONResponse({"success":False,"message":"L'email n'est pas valide"})

#la fonction qui verifie le code envoyé a l'utlisateur
async def verify_otp(email: str, request:Request):
    data=await request.json()
    otp=data.get("otp")
    user=await db.users.find_one({"email": email})
    if user and user.get("otp") == otp:
        await db.users.update_one({"email": email}, {"$unset": {"otp": ""}})
        return JSONResponse({"success":True,"message":"L'OTP est valide"})
    else:
        return JSONResponse({"success":False,"message":"L'OTP n'est pas valide"})

#la fonction qui permet a l'utilsateur de modifier don mot de passe
async def reset_password(email: str, request: Request):
    data = await request.json()
    new_password = data.get("new_password")
    user = await db.users.find_one({"email": email})
    if user:
        await db.users.update_one({"email": email}, {"$set": {"password_hash": hash_password(new_password)}})
        return JSONResponse({"success": True, "message": "Le mot de passe a été réinitialisé avec succès"})
    else:
        return JSONResponse({"success": False, "message": "Utilisateur non trouvé"})

