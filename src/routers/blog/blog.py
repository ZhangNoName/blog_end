from fastapi import APIRouter

router = APIRouter()

@router.get("/blogs/")
async def get_blogs():
    return [{"title": "Blog 1"}, {"title": "Blog 2"}]

@router.get("/blogs/{blog_id}")
async def get_blog(blog_id: int):
    return {"title": "Blog 1", "id": blog_id}
