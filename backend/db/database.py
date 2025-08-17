# 配置数据库连接和会话管理
# 依赖注入模式管理数据库会话,自动的连接池管理
# 使用sqlalchemy创建数据库引擎
# 使用create_engine创建引擎,用于与数据库交互
from sqlalchemy import create_engine
# 使用sessionmaker创建会话,用于与数据库交互
from sqlalchemy.orm import sessionmaker
# 使用declarative_base创建基类,所有数据模型都需要继承它，用于定义数据表结构
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建ORM基类
Base = declarative_base()

# 🔄 数据库会话依赖注入
# 确保请求结束后正确关闭数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 创建数据库表,首次运行时需要基于数据模型创建表，启动时执行
def create_tables():
    Base.metadata.create_all(bind=engine)