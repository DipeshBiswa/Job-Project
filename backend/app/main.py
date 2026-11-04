import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.Model.user import User
from app.Controller.user_controller import router as user_router
from fastapi.middleware.cors import CORSMiddleware

"""
entry point for the backend, creates the FastAPI app, initalizes MongoDB, registers routes
and allows frontend to call the API

"""



#connects to MongoDB when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    )

    #initalizes Beanie, lets python work with MongoDB through models 
    await init_beanie(
        database=client["job_project"],
        document_models=[User]
    )
    yield
    await client.close()

#creates API and tell FastAPI to use startup/shutdown process 
app = FastAPI(lifespan=lifespan)

#connect the routes from user_controller to the application
app.include_router(user_router)

@app.get("/")
async def home():
    return {"message" : "Job Project API is running"}


#CORS, tells the browser that these two frontend addresses can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

