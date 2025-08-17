#在这里将.env文件中的配置加载到环境变量中，以便在各处引用。这是标准做法
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = ""
    # POIXE API 配置
    POIXE_API_KEY: str
    POIXE_BASE_URL: str

    # 将ALLOWED_ORIGINS字符串转换为列表
    @field_validator("ALLOWED_ORIGINS")
    def validate_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []

    # 配置文件设置
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()