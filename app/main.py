from fastapi import FastAPI
from app.routers.images import effects
import uvicorn

app = FastAPI()
app.include_router(effects.router)

@app.get("/")
async def root():
    return {"data": "Blackcore Iris API"}
