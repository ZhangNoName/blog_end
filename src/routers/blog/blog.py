from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

router = APIRouter()

# 初始化 Motor 客户端
client = AsyncIOMotorClient("mongodb://localhost:27017")  # 这里替换成你的 MongoDB 连接字符串
db = client.blog_db  # 这里替换成你的数据库名称
blog_collection = db.blogs  # 这里替换成你的集合名称

# Pydantic 模型
class BlogModel(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    author: Optional[str] = Field(default=None, description="创建者名称")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class BlogResponseModel(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    content: str
    author: Optional[str]
    created_at: Optional[datetime]

# 获取所有博客
@router.get("/blogs/")
async def get_blogs():
    blogs = await blog_collection.find().to_list(length=100)
    return blogs

# 获取单个博客
@router.get("/blogs/{id}", response_model=BlogResponseModel)
async def get_blog(id: str):
    try:
        obj_id = PyObjectId.validate(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    blog = await blog_collection.find_one({"_id": obj_id})
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    blog["_id"] = str(blog["_id"])
    return BlogResponseModel(**blog)

# 添加博客
@router.post("/blogs/")
async def add_blog(blog: BlogModel = Body(...)):
    blog_dict = blog.dict()
    blog_dict["_id"] = ObjectId()
    result = await blog_collection.insert_one(blog_dict)
    if result.inserted_id:
        return {"id": str(result.inserted_id), "message": "Blog added successfully"}
    raise HTTPException(status_code=500, detail="Failed to add blog")
