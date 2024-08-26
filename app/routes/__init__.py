from fastapi import APIRouter

# 라우터 import
from .job_posts import router as job_posts_router
from .edu_posts import router as edu_posts_router

# 라우터 module-level variables로 설정
job_posts = job_posts_router
edu_posts = edu_posts_router
