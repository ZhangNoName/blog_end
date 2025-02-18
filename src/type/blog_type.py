from datetime import datetime
from typing import List, Optional, Union
import uuid
from pydantic import BaseModel, Field

class Blog(BaseModel):
    id: int = Field(default_factory=lambda: str(uuid.uuid4()), description="博客的唯一标识符")
    title: str = Field(..., description="博客标题")
    content: str = Field(..., description="博客内容")
    author: Optional[str] = Field(default="zxy", description="作者")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
class BlogBase(BaseModel):
    id: int = Field(default_factory=lambda: str(uuid.uuid4()), description="博客的唯一标识符")
    title: str = Field(..., description="博客标题")
    author: Optional[str] = Field(default="zxy", description="作者")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    abstract: str = Field(..., description="文章摘要")
    view_num: int = Field(0, description="浏览次数")
    comment_num: int = Field(0, description="评论次数")
    byte_num: int = Field(0, description="评论次数")
    tag: Optional[str] = Field(..., description="标签")
    category: Optional[str] = Field(..., description="分类")

class BlogCreate(Blog):
    id: Optional[int] = Field(None, description="博客的唯一标识符")
    abstract: str = Field(..., description="文章摘要")
    tag: List[str] = Field(..., description="文章标签（多个）")  # 标签变为数组
    category: str = Field(..., description="分类")
