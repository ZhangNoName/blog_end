from pymongo import MongoClient
import redis.asyncio as redis

# MongoDB配置
MONGO_URL = "mongodb://localhost:27017/"
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["blog"]
articles_collection = mongo_db["articles"]
comments_collection = mongo_db["comments"]
logs_collection = mongo_db["logs"]

# Redis配置
REDIS_URL = "redis://localhost"
redis_client = redis.from_url(REDIS_URL)

# 在应用启动时连接数据库
async def connect_db():
    print("Indexes created")
    pass

# 在应用关闭时断开数据库连接
async def close_db():
    # 关闭MongoDB连接
    mongo_client.close()
    # 关闭Redis连接
    await redis_client.close()
