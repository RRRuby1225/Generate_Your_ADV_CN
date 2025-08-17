#核心业务逻辑，负责AI故事生成和数据处理

from sqlalchemy.orm import Session

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story,StoryNode
from core.models import StoryLLMResponse,StoryNodeLLM
from dotenv import load_dotenv
from core.config import settings

class StoryGenerator:

    @classmethod
    def _get_llm(cls):
        #创建OpenAI客户端
        return ChatOpenAI(
            model="gpt-3.5-turbo:free",
            api_key=settings.POIXE_API_KEY,
            base_url=settings.POIXE_BASE_URL
        )

    '''
        生成故事
        1. 创建OpenAI客户端
        2. 创建故事解析器
        3. 创建提示模板
        4. 调用OpenAI API生成故事
        5. 处理故事结构
        6. 保存故事到数据库
    '''
    @classmethod
    def generate_story(cls, db: Session, session_id: str,theme:str = "fantasy")->Story:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            ("system", STORY_PROMPT),
            ("human", "Create the story with theme: {theme}"),
        ]).partial(format_instructions=story_parser.get_format_instructions())

        raw_response = llm.invoke(prompt.invoke({"theme": theme}))
        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content

        story_structure = story_parser.parse(response_text)

        story_db = Story(title=story_structure.title,session_id=session_id)
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(db,story_db.id,root_node_data,is_root=True)


        db.commit()
        return story_db

    '''
        # 🌳 递归处理故事节点（关键算法）：
        # 1. 创建当前节点
        # 2. 如果有选项，遍历每个选项
        # 3. 对每个选项的nextNode递归调用此函数
        # 4. 将子节点ID存入当前节点的options字段
    '''
    @classmethod
    def _process_story_node(cls,db:Session,story_id:int,node_data:StoryNodeLLM,is_root:bool=False)->StoryNode:
        # 1️⃣ 创建当前节点记录
        node = StoryNode(
            story_id=story_id,
            content=node_data.content if hasattr(node_data,"content") else node_data["content"],
            is_root = is_root,
            is_ending = node_data.isEnding if hasattr(node_data,"isEnding") else node_data["isEnding"],
            is_winning_ending = node_data.isWinningEnding if hasattr(node_data,"isWinningEnding") else node_data["isWinningEnding"],
            options = []
        )
        db.add(node)
        db.flush()

        # 2️⃣ 如果不是结束节点且有选项
        if not node.is_ending and (hasattr(node_data,"options") and node_data.options):
            options_list = []
            
            # 3️⃣ 遍历每个选项
            for option_data in node_data.options:
                next_node = option_data.nextNode
            
                if isinstance(next_node,dict):
                    next_node = StoryNodeLLM.model_validate(next_node)
                
                # 4️⃣ 递归处理子节点
                child_node = cls._process_story_node(db,story_id,next_node,is_root=False)

                # 5️⃣ 保存选项信息，引用子节点ID
                options_list.append({
                    "text":option_data.text,
                    "node_id":child_node.id
                })
            # 6️⃣ 更新当前节点的选项
            node.options = options_list

        db.flush()
        return node



