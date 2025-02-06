from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Base"])
async def read_root():
    return {"message": "Welcome to the base API"}
@router.get("/base", tags=["Base"])
async def base_info():
    """
    基本信息
    """
    return "获取当前的基本信息：博客数目"
