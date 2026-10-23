import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie

from Model.user import User
from Controller.user_controller import router as user_router

from fastapi.middleware.cors import CORSMiddleware





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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

