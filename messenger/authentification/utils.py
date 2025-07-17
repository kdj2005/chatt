import httpx
import random
from manager.manager import manager
from database import db
import hashlib

#la fonction pour envoyer un email de bienvenue a l'utilsateur
async def send_bienvenue(email,name):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/sendemail/welcome", json={"to": email, "name": name},timeout=20)
        return response

#la fonction qui envoie le code a 5 chiffre a l'email de l'utilsateur       
async def send_otp(email, otp):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3000/sendemail/otp", json={"to": email, "otp": otp})
        return response

#la fonction qui génère le code a 5 chiffre
def generate_otp():
    return str(random.randint(10000,99999))

#la fonction qui hash le mot de passe  avant la sauvegarde dans la db
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

#la fonction qui creer un user et le sauvegarde dans la db
async def create_user(email: str, password: str, pseudo: str = ""):
    if await db.users.find_one({"email": email}):
        return False
    await db.users.insert_one(user_dict(email, hash_password(password), pseudo))
    return True

#la fonction qui permet la comparaison du mot de passe lors du login
async def authenticate_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if user and user["password_hash"] == hash_password(password):
        return True
    return False