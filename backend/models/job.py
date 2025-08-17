#管理故事生成任务的状态
'''
# 💡 状态管理：
- pending: 待处理
- processing: 处理中
- completed: 已完成
- failed: 处理失败
'''

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.database import Base

class StoryJob(Base):
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    #于存储本任务生成的故事id，nullable=True允许此字段为空
    story_id = Column(Integer,nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    

