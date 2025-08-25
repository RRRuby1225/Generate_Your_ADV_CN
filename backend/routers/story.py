import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db
from models.story import Story
from models.job import StoryJob
from schemas.story import CreateStoryRequest, CompleteStoryResponse
from schemas.job import StoryJobResponse
from core.story_service import StoryService


router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id:Optional[str]=Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


@router.post("/create",response_model=StoryJobResponse)
def create_story(
    request:CreateStoryRequest,
    background_tasks:BackgroundTasks,
    response:Response,
    session_id:str=Depends(get_session_id),
    db:Session=Depends(get_db)):

    response.set_cookie(key="session_id",value=session_id,httponly=True)

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme = request.theme,
        status = "pending"
    )
    db.add(job)
    db.commit()

    background_tasks.add_task(StoryService.generate_story_task, job_id=job_id, session_id=session_id, theme=request.theme)

    return job


@router.get("/{story_id}/complete",response_model=CompleteStoryResponse)
def get_complete_story(story_id:int,db:Session=Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404,detail="Story not found")
    
    complete_story = StoryService.build_complete_story_tree(db, story)

    return complete_story