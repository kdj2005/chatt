from fastapi import FastAPI
from authentification.route_authentification import router as auth_router
from fastapi.responses import FileResponse
from chat.chat_route import router as chat_router
from group.group_route import router as group_router
from notification.route_notification import router as notification_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/chat")
app.include_router(group_router, prefix="/group")
app.include_router(notification_router, prefix="/notification")



app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/home.html")
@app.get("/home")
async def home_page():
    return FileResponse("static/o.html")

@app.get("/login")
async def login_page():
    return FileResponse("static/connexion.html")

@app.get("/register")
async def register_page():
    return FileResponse("static/inscription.html")

@app.get("/otp")
async def otp_page():
    return FileResponse("static/otp.html")

@app.get("/reset-password")
async def reset_password_page():
    return FileResponse("static/reset-password.html")

@app.get("/jeux")
async def jeux_page():
    return FileResponse("static/jeu.html")

@app.get("/forgot-password")
async def forgot_password_page():
    return FileResponse("static/forgot-password.html")

