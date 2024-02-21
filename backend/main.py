from fastapi import FastAPI
from src.routers import media_router, command_router


app = FastAPI()

app.include_router(media_router, prefix="/media", tags=["media"])
app.include_router(command_router, prefix="/command", tags=["command"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
