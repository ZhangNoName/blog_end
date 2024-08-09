# app/database.py
from pymongo import MongoClient

MONGO_DETAILS = "mongodb://localhost:27017"  # 替换为你的 MongoDB 连接字符串

client = MongoClient(MONGO_DETAILS)
database = client.blog_database
blog_collection = database.get_collection("blogs")
