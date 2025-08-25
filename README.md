# FastAPI+React+OpenAI API 全栈开发

✅ FastAPI  
✅ SQLAlchemy  
✅ React + Vite  
✅ LangChain + OpenAI  
⚠️ SQLite  
⚠️ 原生CSS  

本项目使用 FastAPI + React 实现了一个 AI 生成的文字冒险游戏。根据 [The Ultimate FastAPI + React Full Stack Project](https://www.youtube.com/watch?v=_1P0Uqk50Ps&list=LL&index=1&t=71s) 视频教程实现，原项目 github 地址为[Choose-Your-Own-Adventure-AI](https://github.com/techwithtim/Choose-Your-Own-Adventure-AI)，适合有一定 Python 和 JS 基础的开发者学习 FastAPI 和 React 全栈开发。  

与原项目不同的地方：  
1.对后端进行了重构，新增了 story_server.py 处理故事生成的业务逻辑、数据库操作和错误处理，使每个模块的职责更清晰。  
2.对提示词进行一定优化，使生成的故事与选项内容更加匹配。  
3.本地化

## 最终运行效果

<img width="1417" height="992" alt="页面1" src="https://github.com/user-attachments/assets/80430875-dc58-43ce-a8d0-9d4860ca42f7" />

<img width="1416" height="1178" alt="页面2" src="https://github.com/user-attachments/assets/06c9cfd3-5670-4c2d-bed2-20cab48c457b" />


## backend 搭建

### 安装环境

#### 1. uv 安装

官方手册 [Installing uv](https://docs.astral.sh/uv/getting-started/installation/)  
我选择的安装方式是

    cd backend
    pip install uv

安装完成后输入

    uv init .
uv init . 会生成 pyproject.toml 和 .python-version 配置文件，可以在文件里修改要安装的 python 版本。__使用 FastAPI 你的 Python 版本必须  >3.6 ， 我使用的版本为 3.12。__  

<img width="480" height="140" alt="初始化" src="https://github.com/user-attachments/assets/4d640dcd-3ba8-4521-9a2b-fc5c10203432" />

#### 2.安装依赖  

    uv add fastapi[all] langchain langchain-openai python-dotenv sqlalchemy uvicorn psycopg2-binary
这样做的主要目的是将这些依赖项保持为项目私有，与系统其他部分隔离。  

如果出现以下警告，会影响uv性能但不会影响项目运行。  

    warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
    If the cache and target directories are on different filesystems, hardlinking may not be supported.
    If this is intentional, set export UV_LINK_MODE=copy or use --link-mode=copy to suppress this warning.
可参考本帖 <https://github.com/astral-sh/uv/issues/7285>

如果下载速度比较慢可以配置国内源，在 pyproject.toml 中输入

    [[index]]
    url = "https://pypi.mirrors.ustc.edu.cn/simple/"
    default = true
如需使用其他镜像源也可自行选择。

安装完成后设置编辑器环境，位置在

    .\.venv\Scripts\python.exe  

### backend 文件结构搭建  

```text
backend/
├─ __init__.py                   # Python包标识文件
├─ .env                          # 环境变量配置文件
├─ .python-version               
├─ main.py                       # 应用程序启动入口，配置所有中间件和路由
├─ pyproject.toml
├─ uv.lock
├─ .venv
├─ core/
│  ├─ __init__.py                
│  ├─ config.py                  # 集中管理所有环境变量和应用配置
│  ├─ models.py                  # 定义AI返回数据的结构化模型，确保数据格式正确
│  ├─ prompts.py                 # 提供标准化的提示词模板
│  ├─ story_generator.py         # 实现AI故事生成的核心算法，专注于AI模型调用
│  └─ story_service.py           # 故事业务服务层，处理数据库操作和业务逻辑编排
├─ db/
│  ├─ __init__.py                
│  └─ database.py                # 管理数据库连接、会话和表结构创建
├─ models/
│  ├─ __init__.py               
│  ├─ job.py                     # 跟踪异步任务的执行状态和结果
│  └─ story.py                   # 定义故事和节点的数据库表结构，实现树状关系存储
├─ routers/
│  ├─ __init__.py                
│  ├─ job.py                     # 提供任务状态查询接口，支持异步处理模式
│  └─ story.py                   # 提供故事创建和获取的REST API接口
└─ schemas/
   ├─ __init__.py                
   ├─ job.py                     # 标准化任务相关API的数据格式
   └─ story.py                   # 定义API的输入输出数据格式
```

### 检查运行

在终端 cd 到 backend ，并运行

    uv run .\main.py

在浏览器输入对应地址可以看到 FastAPI 自动生成的 API 文档界面。  

    http://localhost:8000/docs
    http://localhost:8000/redoc

## backend项目结构

*⚠️以下图均由AI生成*

### 数据表结构

```mermaid
%%{init: {
    'theme': 'dark',
    'themeVariables': {
        'actorBorder': '#2196f3',
        'actorBackground': '#212121',
        'noteBorder': '#2196f3',
        'noteBackground': '#212121'
    }
}}%%
erDiagram
    %% Story 和 StoryNode 的一对多关系
    Story ||--o{ StoryNode : "一对多：一个故事包含多个节点"
    
    %% StoryJob 和 Story 的一对一关系（可空）
    StoryJob ||--o| Story : "一对一：一个任务生成一个故事"
    
    %% StoryNode 的自引用一对多关系
    StoryNode ||--o{ StoryNode : "一对多：一个节点可以指向多个后续节点"
    
    Story {
        int id PK
        string title
        string session_id
        datetime created_at
    }
    StoryNode {
        int id PK
        int story_id FK "关联Story.id"
        string content
        boolean is_root
        boolean is_ending
        boolean is_winning_ending
        json options "包含node_id引用其他节点"
    }
    StoryJob {
        int id PK
        string job_id
        string session_id
        string theme
        string status
        int story_id FK "nullable, 关联Story.id"
        string error "nullable"
        datetime created_at
        datetime completed_at "nullable"
    }
```

### backend分层架构结构图

```mermaid
%%{init: {
    'theme': 'dark',
    'themeVariables': {
        'actorBorder': '#2196f3',
        'actorBackground': '#212121',
        'noteBorder': '#2196f3',
        'noteBackground': '#212121',
        'activationBackground': '#2196f3'
    }
}}%%
sequenceDiagram
    participant C as 客户端
    participant R as Routers层
    participant S as Schemas层
    participant Core as Core层
    participant M as Models层
    participant DB as 数据库

    Note over C,DB: 完整分层架构数据流向
    
    C->>R: HTTP请求
    activate R
    Note over R: 职责：接收请求、调用业务逻辑、返回响应
    
    R->>S: 数据验证
    activate S
    Note over S: 职责：验证输入格式、格式化输出数据
    S-->>R: 验证结果
    deactivate S
    
    R->>Core: 调用核心业务逻辑
    activate Core
    Note over Core: 职责：AI故事生成、配置管理、提示词模板、数据模型定义
    
    Core->>M: 数据操作
    activate M
    Note over M: 职责：数据库CRUD操作、ORM映射
    M->>DB: SQL执行
    DB-->>M: 数据库结果
    M-->>Core: 数据对象
    deactivate M
    
    Core-->>R: 业务处理结果
    deactivate Core
    
    R->>S: 响应格式化
    activate S
    S-->>R: 格式化数据
    deactivate S
    
    R-->>C: HTTP响应
    deactivate R
```

### backend 时序图

```mermaid
%%{init: {
    'theme': 'dark',
    'themeVariables': {
        'actorBorder': '#2196f3',
        'actorBackground': '#212121',
        'noteBorder': '#2196f3',
        'noteBackground': '#212121',
        'activationBackground': '#2196f3'
    }
}}%%
sequenceDiagram
    participant C as 客户端
    participant API as FastAPI Router
    participant BT as 后台任务
    participant AI as OpenAI API
    participant DB as Database

    C->>API: POST /stories/create
    activate API
    Note over API: create_story()
    
    API->>DB: 创建 StoryJob 记录（status: pending）
    activate DB
    DB-->>API: 确认创建
    
    API-->>C: 返回 job_id
    
    API->>BT: 添加后台任务 generate_story_task()
    deactivate API
    
    activate BT
    BT->>DB: 创建新的数据库会话
BT->>DB: 查询job记录是否存在
alt job不存在
    BT-->>BT: 直接返回
else job存在
    BT->>DB: 更新任务状态为 processing
end
    
    Note over BT: StoryGenerator.generate_story()
    BT->>AI: 调用 AI 生成故事
    activate AI
    Note over AI: ChatOpenAI.invoke()
    AI-->>BT: 返回 JSON 格式故事数据
    deactivate AI
    
    BT->>DB: 创建 Story 记录
    
    Note over BT: _process_story_node(root_node, is_root=True)
    BT->>DB: 创建根节点记录
    DB-->>BT: 返回根节点 ID

    loop 递归处理所有节点
        Note over BT: _process_story_node() 递归调用
        BT->>DB: 创建当前节点记录
        DB-->>BT: 返回节点 ID
        BT->>DB: 更新父节点的 options 数组
        Note over BT: 对非结局节点的每个选项重复此过程
    end
    
    BT->>DB: 更新任务状态为 completed
    deactivate BT
    
    loop 轮询任务状态
        C->>API: GET /jobs/{job_id}
        activate API
        Note over API: get_job_status()
        API->>DB: 查询任务状态
        DB-->>API: 返回任务信息
        API-->>C: 返回任务状态
        deactivate API
    end
    
    C->>API: GET /stories/{id}/complete
    activate API
    Note over API: get_complete_story()
    API->>DB: 查询故事和节点数据
    DB-->>API: 返回数据
    
    Note over API: build_complete_story_tree()
    
    API-->>C: 返回完整故事数据
    deactivate API
    deactivate DB
```

## frontend 搭建

### 安装环境

`安装前需要确保你的环境中已安装 Node.js`

终端 cd 到项目 __根目录__

#### 1. 使用 Vite 创建 React 项目

    npm create vite@latest frontend -- --template react

cd 到 __frontend__

#### 2. 安装 package.json 中定义的所有依赖

    npm install

#### 3. 安装 axios HTTP 客户端库

    npm install axios

#### 4. 安装 dom 库，这个库用于实现不同页面的路由跳转

    npm install react-router-dom

#### 5. 运行

    npm run dev

### frontend 文件结构

```
frontend/
├─ eslint.config.js           
├─ index.html                           # 应用入口 HTML 文件
├─ package.json               
├─ vite.config.js             
└─ src/
   ├─ App.css                           # 全局样式表
   ├─ App.jsx                           # React 应用主组件
   ├─ index.css                         # 入口样式表，通常用于全局样式
   ├─ main.jsx                          # 应用入口文件，挂载 React 组件
   ├─ util.js                           # 工具函数文件
   └─ components/
      ├─ LoadingStatus.jsx              # 显示加载状态组件
      ├─ StoryGame.jsx                  # 主界面组件
      ├─ StoryGenerator.jsx             # 故事生成器组件
      ├─ StoryLoader.jsx                # 故事加载组件
      └─ ThemeInput.jsx                 # 主题输入组件
```

### frontend 时序图

*⚠️下图由AI生成*

```mermaid
%%{init: {
    'theme': 'dark',
    'themeVariables': {
        'actorBorder': '#2196f3',
        'actorBackground': '#212121',
        'noteBorder': '#2196f3',
        'noteBackground': '#212121',
        'activationBackground': '#2196f3'
    }
}}%%
sequenceDiagram
    participant U as 用户
    participant G as StoryGenerator
    participant L as LoadingStatus
    participant B as Backend API
    participant S as StoryLoader
    participant Game as StoryGame
    
    U->>G: 输入故事主题
    activate G
    Note over G: ThemeInput 组件验证输入
    G->>L: 显示加载状态
    activate L
    G->>B: POST /stories/create
    activate B
    B-->>G: 返回 job_id
    
    loop 每5秒
        G->>B: GET /jobs/{job_id}
        B-->>G: 返回任务状态
    end
    
    B-->>G: 任务完成，返回 story_id
    deactivate B
    G->>G: 导航到 /story/{id}
    deactivate L
    deactivate G
    
    activate S
    S->>B: GET /stories/{id}/complete
    activate B
    B-->>S: 返回完整故事数据
    deactivate B
    S->>Game: 传递故事数据
    deactivate S
    
    activate Game
    Game-->>U: 展示故事内容
    
    loop 直到到达结局
        U->>Game: 选择故事选项
        Game->>Game: 更新当前节点
        alt 是结局节点
            Game-->>U: 显示结局信息
            U->>Game: 点击重新开始
            Game->>Game: 重置到根节点
        else 不是结局节点
            Game-->>U: 显示新的故事内容和选项
        end
    end
    
    U->>Game: 点击创建新故事
    Game->>G: 导航到首页
    deactivate Game
    
    Note over U,Game: 整个故事流程结束
```


