from fastapi import APIRouter, Depends, Query
from app.models import EduPostModel
from app.schemas import EduPostCollection, SearchCriteria
from app.database import eud_post_collection

router = APIRouter()

@router.get("/", response_model=EduPostCollection)
async def list_edu_posts():
    edu_posts_cursor = eud_post_collection.find()
    edu_posts = await edu_posts_cursor.to_list(length=None)
    
    total_count = await eud_post_collection.count_documents({})
    
    return EduPostCollection(
        edu_posts=edu_posts,
        total_count=total_count
    )

@router.get("/search", response_model=EduPostCollection)
async def search_edu_posts(
    criteria: SearchCriteria = Depends(),
    start: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query('date', enum=['date'])
):
    query = {}
    
    total_count = await eud_post_collection.count_documents(query)
    
    edu_posts_cursor = eud_post_collection.find(query).skip(start).limit(limit)
    edu_posts = await edu_posts_cursor.to_list(length=limit)

    if sort == 'date':
        edu_posts.sort(key=lambda post: post.get("date", ""), reverse=False)
        
    return EduPostCollection(
        edu_posts=edu_posts,
        total_count=total_count,
    )
