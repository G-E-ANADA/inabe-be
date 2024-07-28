import os
from typing import List, Optional

import certifi
import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv  # Add this import
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator
from pymongo import ReturnDocument
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing_extensions import Annotated

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from environment variables
ca = certifi.where()
base_uri = os.getenv("MONGODB_URI")
if not base_uri:
    raise ValueError("MONGODB_URI environment variable is not set")

uri = f"{base_uri}?retryWrites=true&w=majority&appName=Cluster0&tlsCAFile={ca}"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI(
    title="Job Posts API",
    summary="A sample application showing how to use FastAPI to add a REST API to a MongoDB collection.",
)

# CORS 설정 추가
origins = os.getenv("CORS_ORIGINS", "").split(",")
if not origins:
    origins = ["http://localhost:4000",
               "http://localhost:1234"]  # Default origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # origins 리스트에 있는 도메인에서 오는 요청을 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용
)

db = client.get_database("InAbleDB")
job_post_collection = db.get_collection("job_posts")

PyObjectId = Annotated[str, BeforeValidator(str)]


class JobPostModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    busplaName: str
    cntctNo: str
    compAddr: str
    empType: str
    enterType: str
    jobNm: str
    offerregDt: str
    regDt: str
    regagnName: str
    reqCareer: str
    reqEduc: str
    rno: str
    rnum: str
    salary: str
    salaryType: str
    termDate: str
    reqMajor: Optional[str]
    envBothHands: str
    envEyesight: str
    envLiftPower: str
    envLstnTalk: str
    envStndWalk: str
    # envHandwork: str
    reqLicens: Optional[str]


class JobPostCollection(BaseModel):
    job_posts: List[JobPostModel]


@app.get(
    "/job_posts/",
    response_description="List all job posts",
    response_model=JobPostCollection,
    response_model_by_alias=False,
)
async def list_job_posts():
    """
    List all of the student data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    job_posts = list(job_post_collection.find())
    return JobPostCollection(job_posts=job_posts)

# uvicorn job_post:app --reload
