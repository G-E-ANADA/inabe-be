from typing import Optional
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from datetime import datetime

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
    reqLicens: Optional[str]
    latitude: str
    longitude: str
    startDate: Optional[datetime]
    endDate: Optional[datetime]
    searchRegion: str
    searchJobCategory: str
    searchEnvBothHands: str
    searchEnvEyesight: str
    searchEnvLiftPower: str
    searchEnvLstnTalk: str
    compLogoUrl: str
    postId: int

class EduPostModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    category: str
    title: str
    organization: str
    date: str
    content: str
    postId: int