from io import BytesIO
import itertools
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import uuid
import time
import json

# 配置 Redis 客户端
r = redis.Redis(host='localhost', port=6379, db=0)


async def log_request(request: Request):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    request_body = await request.body()
    request_data = {
        "request_id": request_id,
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": request_body.decode()  # 解码请求体
    }
    r.set(f"request:{request_id}", json.dumps(request_data))
    return request_id, start_time  # 只返回两个值

async def log_response(request_id, start_time, response: Response):
    end_time = time.time()
    
    if isinstance(response, StreamingResponse):
        original_body_iterator = response.body_iterator
        body = BytesIO()
        async def logging_body_iterator():
            async for chunk in original_body_iterator:
                body.write(chunk)
                yield chunk
        response.body_iterator = logging_body_iterator()
        body.seek(0)
        body_content = body.read()
    else:
        body_content = await response.body()
    
    response_data = {
        "request_id": request_id,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": body_content.decode(),  # 解码响应体
        "duration": end_time - start_time
    }
    r.set(f"response:{request_id}", json.dumps(response_data))

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id, start_time = await log_request(request)
        response = await call_next(request)

        if isinstance(response, StreamingResponse):
            original_body_iterator = response.body_iterator
            body = BytesIO()
            async def logging_body_iterator():
                async for chunk in original_body_iterator:
                    body.write(chunk)
                    yield chunk
            response.body_iterator = logging_body_iterator()
            body.seek(0)
            await log_response(request_id, start_time, response)
        else:
            await log_response(request_id, start_time, response)

        return response

def get_logs(request_id):
    request_log = r.get(f"request:{request_id}")
    response_log = r.get(f"response:{request_id}")
    if not request_log or not response_log:
        return None
    return {
        "request": json.loads(request_log),
        "response": json.loads(response_log)
    }
