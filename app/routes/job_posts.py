from fastapi import APIRouter, Depends, Query
from typing import List
from app.models import JobPostModel
from app.schemas import JobPostCollection, SearchCriteria
from app.database import job_post_collection
from app.utils import str_to_datetime

router = APIRouter()

@router.get("/", response_model=JobPostCollection)
async def list_job_posts():
    job_posts_cursor = job_post_collection.find()
    job_posts = await job_posts_cursor.to_list(length=None)
    
    total_count = await job_post_collection.count_documents({})
    
    return JobPostCollection(
        job_posts=job_posts,
        total_count=total_count
    )

@router.get("/search", response_model=JobPostCollection)
async def search_job_posts(
    criteria: SearchCriteria = Depends(),
    start: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query('endDate', enum=['regDt', 'endDate'])
):
    query = {}
    
    if criteria.empType:
        query["empType"] = criteria.empType
    if criteria.enterType:
        query["enterType"] = criteria.enterType
    if criteria.searchRegion:
        query["searchRegion"] = criteria.searchRegion
    if criteria.searchJobCategory:
        query["searchJobCategory"] = criteria.searchJobCategory
    if criteria.searchEnvEyesight:
        query["searchEnvEyesight"] = criteria.searchEnvEyesight
    if criteria.searchEnvLstnTalk:
        query["searchEnvLstnTalk"] = criteria.searchEnvLstnTalk
    if criteria.searchEnvLiftPower:
        query["searchEnvLiftPower"] = criteria.searchEnvLiftPower
    if criteria.searchEnvBothHands:
        query["searchEnvBothHands"] = criteria.searchEnvBothHands

    total_count = await job_post_collection.count_documents(query)
    
    job_posts_cursor = job_post_collection.find(query).sort(
        "endDate" if sort == "endDate" else "regDt", 
        1 if sort == "endDate" else -1
    ).skip(start).limit(limit)
    
    job_posts = await job_posts_cursor.to_list(length=limit)

    print(f"Sorting by: {'endDate' if sort == 'endDate' else 'regDt'}")
    print(f"Order: {1 if sort == 'endDate' else -1}")

    return JobPostCollection(
        job_posts=job_posts,
        total_count=total_count,
    )
