from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class Blog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="博客的唯一标识符")
    title: str = Field(..., description="博客标题")
    content: str = Field(..., description="博客内容")
    author: Optional[str] = Field(default="zxy", description="作者")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
