#定义与OpenAI API交互的数据模型,确保AI返回的JSON结构符合预期格式

from typing import List, Optional, Dict, Any
from click import option
from pydantic import BaseModel, Field

#故事选项模型
class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the option that the user can choose")
    nextNode:Dict[str, Any] = Field(description="the next node content and options")

# 故事节点模型  
class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    isEnding: bool = Field(description="Whether the node is an ending node")
    isWinningEnding: bool = Field(description="Whether the node is a winning ending node")
    options : Optional[List[StoryOptionLLM]] = Field(default=None, description="The options for this node")

# 完整故事响应
class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story")