from fastapi import FastAPI
from app.routers.images import effects
import uvicorn

app = FastAPI()
app.include_router(effects.router)

@app.get("/")
async def root():
    return {"data": "Blackcore Iris API"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    main()