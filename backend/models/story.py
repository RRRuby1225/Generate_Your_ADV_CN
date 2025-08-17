# 定义故事相关的数据库表结构

# sqlalchemy 是python中用于操作数据库的库,它提供了一个对象关系映射(ORM)层,
# 允许我们使用python类来定义数据库表结构,并自动生成SQL语句,从而避免手动编写SQL语句
from sqlalchemy import Column, Integer, String, DateTime,Boolean,ForeignKey,JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Story(Base):
    # __tablename__定义了数据库表的名称
    # 在这里，表名为"stories"，这将映射到数据库中的一个表。
    __tablename__ = "stories"
    # column代表数据库中的一个字段（列）。每个字段都有相应的数据类型。
    # 这符合数据库的建表规范，行代表一个实体，列代表实体的值。
    #每个story都有唯一的id，并作为主键。主键意味着该字段是唯一的，不能重复。索引意味着该字段可以用于快速查找。
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    #追踪每个创建story的的用户会话，用于关联用户和story
    session_id = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    
    # 一对多关系,一个story可以有多个节点
    nodes = relationship("StoryNode", back_populates="story")

class StoryNode(Base):
    #story的节点表，每个节点代表故事的一个部分
    __tablename__ = "story_nodes"
    id = Column(Integer, primary_key=True, index=True)
    # 外键，关联到story表的id
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    # 节点内容
    content = Column(String)
    #开始节点
    is_root = Column(Boolean, default=False)
    #结束节点
    is_ending = Column(Boolean, default=False)
    #获胜结局节点
    is_winning_ending = Column(Boolean, default=False)
    #选项节点，JSON类型
    options = Column(JSON, default=list)
    #多对一关系,一个节点属于一个故事
    story = relationship("Story", back_populates="nodes")