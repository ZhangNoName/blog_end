from fastapi import FastAPI, Query
from typing import Union
from enum import Enum
from pydantic import BaseModel
import uvicorn

from user.login import router as user_router
app = FastAPI()
app.include_router(user_router)
if __name__ == '__main__':
    print('现在是主线程，运行这里',end='\n')
    # 启动时设置host和post
    
    uvicorn.run(app="main:app",host="0.0.0.0",port=8000,reload=True)

class UserType(str,Enum):
    student= 'edu'
    student2 ='edu2'
    

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items")
async def read_item(skip: int = 0, limit: int | None = None):
    if limit:
        return  fake_items_db[skip : skip + limit]
    return fake_items_db[skip : ]

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    if item.price == 0:
        return {
            "detail":'价格不为0'
        }
    return item
    
