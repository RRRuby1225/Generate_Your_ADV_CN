'''
定义故事相关的API数据格式
- 使用Pydantic进行数据验证
- from_attributes=True支持ORM对象转换
- 清晰的请求/响应分离
'''

from typing import List, Optional,Dict
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy.orm import session

# 故事选项模型
class StoryOptionSchema(BaseModel):
    text: str
    node_id: Optional[int] = None

# 故事节点基础模型
#当类名中包含Base时，表示这是一个基类，用于定义其他类的公共属性
class StoryNodeBase(BaseModel):
    content: str
    is_ending : bool = False
    is_winning_ending : bool = False

# 完整故事节点响应模型
#当类名中包含Response时，表示这是一个响应模型，用于定义API的返回值
class CompleteStoryNodeResponse(StoryNodeBase):
    id : int
    options : List[StoryOptionSchema] = []

    # from_attributes = True  # 这样做是错误的！
    # 这会被 Pydantic 当作一个字段，而不是配置
    #正确的配置方法：在Config类中设置
    class Config:
        #from_attributes = True 是 Pydantic v2 中的一个配置选项，它告诉 Pydantic 可以从具有属性的对象（如 SQLAlchemy ORM 模型实例）创建 Pydantic 模型实例。
        from_attributes = True
    
# 故事基础模型
class StoryBase(BaseModel):
    title : str
    session_id : Optional[str] = None

    class Config:
        from_attributes = True

#创建故事请求模型
class CreateStoryRequest(BaseModel):
    theme : str
    
# 完整故事响应模型
class CompleteStoryResponse(StoryBase):
    id : int
    created_at : datetime
    root_node : CompleteStoryNodeResponse
    all_nodes : Dict[int,CompleteStoryNodeResponse]

    class Config:
        from_attributes = True

