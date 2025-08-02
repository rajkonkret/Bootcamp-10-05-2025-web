from fastapi import FastAPI
from models import User

app = FastAPI()

user_db = []


@app.get("/users/")
def get_users():
    return {"users": user_db}


@app.post("/users/")
def create_user(user: User):
    user_db.append(user)
    return {"message": "User created!", "user": user}
# {
#   "message": "User created!",
#   "user": {
#     "id": 0,
#     "name": "Radek",
#     "email": "radek@radek.pl"
#   }
# }

# {
#   "users": [
#     {
#       "id": 0,
#       "name": "Radek",
#       "email": "radek@radek.pl"
#     }
#   ]
# }