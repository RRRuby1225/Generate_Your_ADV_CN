#查询任务处理状态

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.job import StoryJobResponse
from models.job import StoryJob


router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


'''
    前端轮询检查任务完成状态
    # 📊 功能：
    # 1. 根据job_id查询任务
    # 2. 返回任务状态和相关信息
    # 3. 包含story_id（如果完成）或错误信息
'''
@router.get("/{job_id}",response_model=StoryJobResponse)
def get_job_status(job_id:str,db:Session=Depends(get_db)):
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    
    return job