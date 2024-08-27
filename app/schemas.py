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
    empType: Optional[str] = None
    enterType: Optional[str] = None
    searchRegion: Optional[str] = None
    searchJobCategory: Optional[str] = None
    searchEnvEyesight: Optional[str] = None
    searchEnvLstnTalk: Optional[str] = None
    searchEnvLiftPower: Optional[str] = None
    searchEnvBothHands: Optional[str] = None