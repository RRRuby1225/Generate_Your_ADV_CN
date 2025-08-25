from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from core.models import StoryLLMResponse, StoryNodeLLM
from core.config import settings
import os


class StoryGenerator:
    @classmethod
    def _get_llm(cls):
        #部署环境中获取openai_api_key和service_url
        openai_api_key = os.getenv("CHOREO_OPENAI_CONNECTION_OPENAI_API_KEY")
        service_url = os.getenv("CHOREO_OPENAI_CONNECTION_SERVICEURL")
        if openai_api_key and service_url:
            return ChatOpenAI(
                model="gpt-3.5-turbo:free",
                api_key=openai_api_key,
                base_url=service_url
            )

        return ChatOpenAI(
            model="gpt-3.5-turbo:free",
            api_key=settings.POIXE_API_KEY,
            base_url=settings.POIXE_BASE_URL
        )

    @classmethod
    def generate_story_structure(cls, theme: str = "fantasy") -> StoryLLMResponse:
        llm = cls._get_llm()
        story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

        prompt = ChatPromptTemplate.from_messages([
            ("system", STORY_PROMPT),
            ("human", "请以主题「{theme}」创作一个中文故事"),
        ]).partial(format_instructions=story_parser.get_format_instructions()).invoke({"theme": theme})

        raw_response = llm.invoke(prompt)

        response_text = raw_response
        if hasattr(raw_response, "content"):
            response_text = raw_response.content
        
        story_structure = story_parser.parse(response_text)
        return story_structure

    @classmethod
    def process_node_data(cls, node_data) -> StoryNodeLLM:
        if isinstance(node_data, dict):
            return StoryNodeLLM.model_validate(node_data)
        return node_data



