''' 🎯 作用：FastAPI应用的主入口点
# 核心功能：
1. 创建FastAPI应用实例
2. 配置CORS中间件（跨域处理）
3. 包含路由模块（stories, jobs）
4. 初始化数据库表
5. 启动ASGI服务器
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import story,job
from db.database import create_tables

'''
最初创建表时字段名是 completed_job
后来代码中改成了 completed_at，但数据库表没有更新
SQLAlchemy 的 create_all() 不会修改已存在的表结构
所以需要手动修改表结构，或者删除数据库文件重新创建（如果数据不重要）
'''
create_tables()

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="API to generate cool stories",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
# 跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

# 包含路由
app.include_router(story.router,prefix=settings.API_PREFIX)

app.include_router(job.router,prefix=settings.API_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)