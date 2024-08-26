from fastapi import FastAPI
from app.database import check_mongo_connection
from app.routes.job_posts import router as job_posts_router
from app.routes.edu_posts import router as edu_posts_router
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="Posts API",
    summary="An API for managing and searching postings, with support for filtering and pagination using FastAPI and MongoDB.",
)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await check_mongo_connection()

# 라우트 등록
app.include_router(job_posts_router, prefix="/job_posts", tags=["Job Posts"])
app.include_router(edu_posts_router, prefix="/edu_posts", tags=["Edu Posts"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
