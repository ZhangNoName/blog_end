# main.py
from fastapi.responses import RedirectResponse
from app_instance import app  # Import the app instance
from src.routers import blog_router

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Include the blog router
app.include_router(blog_router)
