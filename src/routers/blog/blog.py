import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from src.controller.blog_manage import BlogManager
from app_instance import app
from src.type.blog_type import Blog


# 创建博客 API 路由
router = APIRouter(prefix="/blogs")

# 注入 BlogManager 依赖
def get_blog_manager() -> BlogManager:
    if not hasattr(app, 'blog'):
        raise HTTPException(status_code=500, detail="Blog manager not initialized")
    return app.blog

# 创建新博客
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(blog: Blog, blog_manager: BlogManager = Depends(get_blog_manager)):
    """
    创建新的博客

    Args:
        blog (Blog): 新博客的数据模型

    Returns:
        dict: 包含新博客 ID 的字典
    """
    logger.info(f'接收到的参数：{blog}')
    
    res = blog_manager.add_blog(blog)
    if res:
        return {"id": blog.id,"success":True}
    else:
        return {"id": None,"success":False}

# 获取指定博客
@router.get("/{blog_id}")
async def get_blog(blog_id: str, blog_manager: BlogManager = Depends(get_blog_manager)):
    """
    获取指定 ID 的博客

    Args:
        blog_id (str): 博客的 ID

    Returns:
        Blog: 博客对象，如果不存在则抛出 404 错误
    """
    blog = blog_manager.get_blog(blog_id)
    # logger.info(f'查找的结果{blog}')
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

# 删除指定博客
@router.delete("/{blog_id}")
async def delete_blog(blog_id: str, blog_manager: BlogManager = Depends(get_blog_manager)):
    """
    删除指定 ID 的博客

    Args:
        blog_id (str): 博客的 ID

    Returns:
        dict: 包含删除成功消息的字典
    """
    if not blog_manager.delete_blog(blog_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
