from fastapi import FastAPI
from app.api.router import api_router
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="VitaGuard API")

Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.get("/")
def home():
    return {"message": "VitaGuard Backend Running"}