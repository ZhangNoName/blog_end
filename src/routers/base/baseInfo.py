from fastapi import APIRouter, Depends, HTTPException
from app_instance import app
from src.controller.tag_manage import TagManager
from src.type.type import ResponseModel

router = APIRouter(prefix="/base",tags=["基础信息"])
# 注入 BlogManager 依赖
def get_tag_manager() -> TagManager:
    if not hasattr(app, 'blog'):
        raise HTTPException(status_code=500, detail="Tag manager not initialized")
    return app.tag
@router.get("/", tags=["基础信息"])
async def read_root():
    return {"message": "Welcome to the base API"}
@router.get("/base", tags=["基础信息"])
async def base_info():
    """
    基本信息
    """
    return "获取当前的基本信息：博客数目"
@router.get("/blog/category", tags=["基础信息"],description="获取博客的种类列表",summary="博客种类列表")
async def get_blog_category(tag_manager: TagManager = Depends(get_tag_manager)):
    """
    获取博客的种类列表
    """
    res = tag_manager.get_category()
    if not res:
        return ResponseModel(code=0, data=None, message="获取category失败")
    return ResponseModel(code=1, data=res, message="获取category列表成功")
@router.get("/blog/tag", tags=["基础信息"] ,description="获取博客的tag列表",summary="博客tag列表")
async def get_tag_list(tag_manager: TagManager = Depends(get_tag_manager)):
    """
    获取博客的tag列表
    """
    res = tag_manager.get_tag()
    if not res:
        return ResponseModel(code=0, data=None, message="获取tag失败")
    return ResponseModel(code=1, data=res, message="获取Tag列表成功")

