from fastapi import FastAPI, Request, Depends, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

import os
from dotenv import load_dotenv

from baza import init_db, get_user, add_user

init_db()

load_dotenv()
app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = "H256"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
BACK_URI = os.getenv("BACK_URI")

print(BACK_URI)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return """
    <html>
    <head><title>Moja Apka</title></head>
    <body>
    <h1>Witaj!</h1>
    <a href='/login'>Zaloguj się przez Google</a>
    </body>
    </html>
    """


@app.get("/login")
def login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
    )
    print(google_auth_url)
    return RedirectResponse(google_auth_url)


