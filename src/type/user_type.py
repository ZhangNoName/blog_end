from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), description="用户的唯一标识符")
    name: str = Field(..., description="昵称")
    age: int = Field(..., description="年龄")
    phone: str = Field(..., description="手机号")
    email: str = Field(..., description="邮箱")
    passwd: str = Field(..., description="密码")
    birth_day: str = Field(..., description="出生日期")
    create_time: Optional[datetime] = Field(default_factory=datetime.now, description="创建时间")
