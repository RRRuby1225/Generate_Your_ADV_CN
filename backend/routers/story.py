# 定义故事相关的API端点
# 异步处理

from logging import root
import uuid #用于生成故事唯一标识符
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException,Cookie,Response,BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db,SessionLocal
from models.story import Story,StoryNode
from models.job import StoryJob
from schemas.story import CreateStoryRequest,CompleteStoryResponse,CompleteStoryNodeResponse
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator


router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id:Optional[str]=Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


'''
    create_story创建故事流程
    # 1. 获取或生成session_id（Cookie）
    # 2. 创建StoryJob记录
    # 3. 启动后台任务生成故事
    # 4. 立即返回job_id给用户

'''
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

    background_tasks.add_task(generate_story_task,job_id = job_id,session_id = session_id,theme = request.theme)

    return job

'''
    生成故事任务
    1. 更新任务状态为processing
    2. 调用StoryGenerator生成故事
    3. 更新任务状态为completed或failed
'''         
def generate_story_task(job_id:str,session_id:str,theme:str):
    db = SessionLocal()

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        if not job:
            return
        try:
            job.status = "processing"
            db.commit()

            story = StoryGenerator.generate_story(db,session_id,theme)

            job.story_id = story.id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()


'''
# 📚 获取完整故事：
    # 1. 查询Story和所有StoryNode
    # 2. 调用build_complete_story_tree()重建树结构
    # 3. 返回完整的故事树
'''
@router.get("/{story_id}/complete",response_model=CompleteStoryResponse)
def get_complete_story(story_id:int,db:Session=Depends(get_db),):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404,detail="Story not found")
    
    complete_story = build_complete_story_tree(db,story)

    return complete_story

'''
    重建完整故事树
    1. 查询所有StoryNode
    2. 构建节点字典
    3. 找到根节点
    4. 返回组织好的树状响应
'''
def build_complete_story_tree(db:Session,story:Story) -> CompleteStoryResponse:
    # 1️⃣ 查询所有节点
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    #2️⃣ 创建节点字典，方便查找
    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options ## 包含{text, node_id}的JSON
        )
        node_dict[node.id] = node_response

    # 3️⃣ 找到根节点
    root_node = next((node for node in nodes if node.is_root),None)
    if not root_node:
        raise HTTPException(status_code=500,detail="missing root node")

    # 4️⃣ 返回完整的树结构
    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict # 前端可以通过node_id查找任意节点
    )