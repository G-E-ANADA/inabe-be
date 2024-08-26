from typing import List, Optional
from pydantic import BaseModel
from .models import JobPostModel, EduPostModel

class JobPostCollection(BaseModel):
    job_posts: List[JobPostModel]
    total_count: int

class EduPostCollection(BaseModel):
    edu_posts: List[EduPostModel]
    total_count: int

class SearchCriteria(BaseModel):
    compAddr: Optional[str] = None
    jobNm: Optional[str] = None
    empType: Optional[str] = None
    envEyesight: Optional[str] = None
    envLiftPower: Optional[str] = None
    envBothHands: Optional[str] = None