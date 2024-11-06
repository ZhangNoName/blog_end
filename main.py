# main.py
from fastapi.responses import RedirectResponse
from app_instance import app  # Import the app instance
from src.routers import blog_router,base_router,user_router

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

routers = [
    blog_router,
    base_router,
    user_router
]

# 使用循环一次性添加所有路由器
for router in routers:
    app.include_router(router)
