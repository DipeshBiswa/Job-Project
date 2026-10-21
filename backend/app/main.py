import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.Model.user import User
from app.Controller.user_controller import router as user_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    )

    await init_beanie(
        database=client["job_project"],
        document_models=[User]
    )
    yield
    await client.close()

    app = FastAPI(lifespan=lifespan)

    app.include_router(user_router)

    @app.get("/")
    async def home():
        return {"message" : "Job Project API is running"}