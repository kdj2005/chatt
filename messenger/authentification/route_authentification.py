from fastapi  import APIRouter,Request
from .logique import register_user,login_user,verify_email,verify_otp,reset_password




router=APIRouter()

 #la route pour creer un compte
@router.post("/register")
async def register(request:Request):
    return await register_user(request)


 #la route pour se connecter
@router.post("/login")
async def login(request:Request):
    return await login_user(request)

#la route pour verifer l'email
@router.post("/verify-email")
async def verifyemail(request:Request):
    return await verify_email(request)

#la route pour verifier le code a 5 chiffre
@router.post('/verify-otp/{email}')
async def otp_verification(email:str,request:Request):
    return await verify_otp(email,request)

#la route pour modifier un mot de passe
@router.post('/reset-password/{email}')
async def resetpassword(email:str,request:Request):
    return await reset_password(email,request)
