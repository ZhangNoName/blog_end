from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from ...database import blog_collection
from typing import Optional

router = APIRouter()

# Pydantic 模型
class BlogModel(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    author: Optional[str] = Field(description="创建者名称",default=None)
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

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, field):
        if schema is not None:
            schema.update(type="string")

class BlogResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    author: str
    created_at: Optional[datetime]

    class Config:
        json_encoders = {ObjectId: str}

# 获取所有博客
@router.get("/blogs/")
async def get_blogs():
    return [{"title": "Blog 1"}, {"title": "Blog 2"}]

# 获取单个博客
@router.get("/blogs/{id}", response_model=BlogResponseModel)
async def get_blog(id: str):
    try:
        # 尝试将传入的字符串 id 转换为 ObjectId
        obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    # 从 MongoDB 中查找文档
    blog = blog_collection.find_one({"_id": obj_id})
    
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # 返回找到的文档
    return BlogResponseModel(**blog)

@router.post("/blogs/")
async def add_blog(blog: BlogModel = Body(...)):
    blog_dict = blog.dict()
    blog_dict["_id"] = ObjectId()  # 添加 MongoDB 的 ObjectId
    result = blog_collection.insert_one(blog_dict)
    if result.inserted_id:
        return {"id": str(result.inserted_id), "message": "Blog added successfully"}
    raise HTTPException(status_code=500, detail="Failed to add blog")
# # 添加博客的接口
# @router.post("/blogs")
# def add_blog(blog: BlogModel = Body(...)):
#     blog_dict = blog.dict()
#     blog_dict["_id"] = ObjectId()  # 添加 MongoDB 的 ObjectId
#     result = blog_collection.insert_one(blog_dict)
#     if result.inserted_id:
#         return BlogResponseModel(**blog_dict)
#     raise HTTPException(status_code=500, detail="博客添加失败")
