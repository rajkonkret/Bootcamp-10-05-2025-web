from fastapi import FastAPI
import uvicorn

# pip install fastapi

app = FastAPI()

#  http://127.0.0.1:8000
@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

# http://127.0.0.1:8000/hello/Radek
@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name.title()}!"}

# if __name__ == '__main__':
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True # tylko w srodowiskach dev, zmiana przeładowuje serwer
#     )
# http://localhost:8000 -> 127.0.0.1
# http://127.0.0.1:8000
#     127.0.0.1:62007 - "GET /ddd HTTP/1.1" 404 Not Found
# uvicorn main:app --reload  - uruchomienie serwera
# OpenAPi - Swagger