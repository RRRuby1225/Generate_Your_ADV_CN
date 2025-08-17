#作用：定义任务相关的API数据格式,统一任务状态查询的响应格式

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StoryJobBase(BaseModel):
    theme : str


class StoryJobResponse(BaseModel):
    job_id : str
    status : str
    created_at : datetime
    story_id : Optional[int] = None
    completed_at : Optional[datetime] = None
    error : Optional[str] = None

    class Config:
        from_attributes = True

# 这里暂时只是给StoryJobBase换了名字，在其它地方使用时保持命名的一致性
class StoryJobCreate(StoryJobBase):
    pass