from typing import List, Optional, Dict, Any
from click import option
from pydantic import BaseModel, Field
class StoryOptionLLM(BaseModel):
    text: str = Field(description="The text of the option that the user can choose")
    nextNode:Dict[str, Any] = Field(description="the next node content and options")

class StoryNodeLLM(BaseModel):
    content: str = Field(description="The main content of the story node")
    isEnding: bool = Field(description="Whether the node is an ending node")
    isWinningEnding: bool = Field(description="Whether the node is a winning ending node")
    options : Optional[List[StoryOptionLLM]] = Field(default=None, description="The options for this node")

class StoryLLMResponse(BaseModel):
    title: str = Field(description="The title of the story")
    rootNode: StoryNodeLLM = Field(description="The root node of the story")