
from io import BytesIO
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json
from .routers import base_router, blog_router
import redis_client
# from .database import connect_db, close_db
app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     await connect_db()

# @app.on_event("shutdown")
# async def shutdown():
#     await close_db()
# class LoggingMiddleware(BaseHTTPMiddleware):
#  async def dispatch(self, request: Request, call_next):
#         request_id, start_time = await redis_client.log_request(request)
#         response = await call_next(request)

#         if isinstance(response, StreamingResponse):
#             original_body_iterator = response.body_iterator
#             body = BytesIO()
#             async def logging_body_iterator():
#                 async for chunk in original_body_iterator:
#                     body.write(chunk)
#                     yield chunk
#             response.body_iterator = logging_body_iterator()
#             await redis_client.log_response(request_id, start_time, response)
#             body.seek(0)
#         else:
#             await redis_client.log_response(request_id, start_time, response)

#         return response

##! 开启日志记录的中间件
##? 123

# app.add_middleware(redis_client.LoggingMiddleware)

# 配置 CORS 允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"], # 允许所有 HTTP 方法
    allow_headers=["*"], # 允许所有 HTTP 头
)
# app.include_router(base_router )
# app.include_router(blog_router)
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/logs/{request_id}")
async def get_logs(request_id: str):
    request_log = r.get(f"request:{request_id}")
    response_log = r.get(f"response:{request_id}")
    if not request_log or not response_log:
        return {"error": "Logs not found"}
    return {
        "request": json.loads(request_log),
        "response": json.loads(response_log)
    }
    
