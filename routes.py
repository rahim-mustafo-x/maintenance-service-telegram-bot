from fastapi import (FastAPI, status)
from model import TokenData
from database import Database

app = FastAPI()
db = Database()

@app.get("/")
async def root():
    print(db.get_tokens())
    return {"message": "Hello World"}

@app.post("/send_code", status_code=status.HTTP_201_CREATED)
async def send_code(data:TokenData):
    try:
        db.add_token(data)
        return {"message": "Code sent successfully"}
    except Exception as e:
        return {"message": str(e)}