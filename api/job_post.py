import os
from typing import List, Optional
import certifi
import motor.motor_asyncio
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from environment variables
ca = certifi.where()
base_uri = os.getenv("MONGODB_URI")
if not base_uri:
    raise ValueError("MONGODB_URI environment variable is not set")

uri = f"{base_uri}?retryWrites=true&w=majority&appName=Cluster0&tlsCAFile={ca}"

# Create a new Motor client and connect to the server
client = motor.motor_asyncio.AsyncIOMotorClient(uri)

# Send a ping to confirm a successful connection


async def check_mongo_connection():
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

app = FastAPI(
    title="Job Posts API",
    summary="An API for managing and searching job postings, with support for filtering and pagination using FastAPI and MongoDB.",
)

# CORS 설정 추가
origins = os.getenv("CORS_ORIGINS", "").split(",")
if not origins:
    origins = ["http://localhost:4000",
               "http://localhost:1234",
               "http://localhost:53673"]  # Default origins

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
    latitude: str
    longitude: str


class JobPostCollection(BaseModel):
    job_posts: List[JobPostModel]


class SearchCriteria(BaseModel):
    compAddr: Optional[str] = None
    jobNm: Optional[str] = None
    empType: Optional[str] = None
    envEyesight: Optional[str] = None
    envLiftPower: Optional[str] = None
    envBothHands: Optional[str] = None


class SearchResponse(BaseModel):
    job_posts: List[JobPostModel]
    total_count: int


@app.on_event("startup")
async def on_startup():
    await check_mongo_connection()


@app.get(
    "/job_posts/",
    response_description="List all job posts",
    response_model=JobPostCollection,
    response_model_by_alias=False,
)
async def list_job_posts():
    job_posts_cursor = job_post_collection.find()
    job_posts = await job_posts_cursor.to_list(length=None)
    return JobPostCollection(job_posts=job_posts)


@app.get(
    "/job_posts/search",
    response_description="Search job posts by criteria with pagination",
    response_model=SearchResponse,
    response_model_by_alias=False,
)
async def search_job_posts(
    criteria: SearchCriteria = Depends(),
    page: int = Query(1, ge=1),  # 페이지 번호, 기본값은 1
    limit: int = Query(10, ge=1, le=100)  # 페이지당 아이템 수, 기본값은 10, 최대 100
):
    query = {}

    if criteria.compAddr:  # 근무 위치 (compAddr)
        query["compAddr"] = {
            "$regex": criteria.compAddr} if criteria.compAddr != "-" else "-"
    if criteria.jobNm:  # 모집 직종 (jobNm)
        query["jobNm"] = criteria.jobNm
    if criteria.empType:  # 고용 형태 (empType)
        query["empType"] = criteria.empType
    if criteria.envEyesight:  # 시력 (envEyesight)
        query["envEyesight"] = criteria.envEyesight
    if criteria.envLiftPower:  # 드는 힘 (envLiftPower)
        query["envLiftPower"] = criteria.envLiftPower
    if criteria.envBothHands:  # 양손 (envBothHands)
        query["envBothHands"] = criteria.envBothHands

    # 총 아이템 수 계산
    total_count = await job_post_collection.count_documents(query)

    # 페이지네이션 적용
    skip = (page - 1) * limit
    job_posts_cursor = job_post_collection.find(query).skip(skip).limit(limit)
    job_posts = await job_posts_cursor.to_list(length=limit)

    # 응답 구성
    return SearchResponse(
        job_posts=job_posts,
        total_count=total_count,
    )

# uvicorn main:app --reload
