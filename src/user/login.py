from fastapi import APIRouter

router = APIRouter()

@router.get("/login/")
async def login():
    return [{"item_id": "item1"}, {"item_id": "item2"}]