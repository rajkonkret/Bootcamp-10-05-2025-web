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

CLIENT_ID = os.getenv("JWT_SECRET")
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