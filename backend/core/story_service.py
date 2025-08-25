# 故事服务层 - 处理故事相关的业务逻辑
from datetime import datetime
from sqlalchemy.orm import Session

from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import CompleteStoryResponse, CompleteStoryNodeResponse
from core.story_generator import StoryGenerator


class StoryService:
    @staticmethod
    def create_story_from_ai(db: Session, session_id: str, theme: str = "fantasy") -> Story:
        story_structure = StoryGenerator.generate_story_structure(theme)
        
        story_db = Story(title=story_structure.title, session_id=session_id)
        db.add(story_db)
        db.flush()
        
        StoryService._process_story_node(db, story_db.id, story_structure.rootNode, is_root=True)
        
        db.commit()
        return story_db
    
    @staticmethod
    def _process_story_node(db: Session, story_id: int, node_data, is_root: bool = False) -> StoryNode:
        processed_node_data = StoryGenerator.process_node_data(node_data)
        
        node = StoryNode(
            story_id=story_id,
            content=processed_node_data.content,
            is_root=is_root,
            is_ending=processed_node_data.isEnding,
            is_winning_ending=processed_node_data.isWinningEnding,
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and processed_node_data.options:
            options_list = []
            
            for option_data in processed_node_data.options:
                next_node = option_data.nextNode
                
                child_node = StoryService._process_story_node(db, story_id, next_node, is_root=False)

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })
            
            node.options = options_list

        db.flush()
        return node
    
    @staticmethod
    def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
        nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

        node_dict = {}
        for node in nodes:
            node_response = CompleteStoryNodeResponse(
                id=node.id,
                content=node.content,
                is_ending=node.is_ending,
                is_winning_ending=node.is_winning_ending,
                options=node.options
            )
            node_dict[node.id] = node_response

        root_node = next((node for node in nodes if node.is_root), None)
        if not root_node:
            raise ValueError("Missing root node")

        return CompleteStoryResponse(
            id=story.id,
            title=story.title,
            session_id=story.session_id,
            created_at=story.created_at,
            root_node=node_dict[root_node.id],
            all_nodes=node_dict
        )

    @staticmethod
    def generate_story_task(job_id: str, session_id: str, theme: str):
        from db.database import SessionLocal
        
        db = SessionLocal()

        try:
            job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
            if not job:
                return
                
            try:
                job.status = "processing"
                db.commit()

                story = StoryService.create_story_from_ai(db, session_id, theme)

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
