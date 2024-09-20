import uuid
from datetime import datetime

from bson import ObjectId
from loguru import logger
from pymongo.cursor import Cursor
from src.database.mongo.mongodb_manage import MongoDBManager
from src.type.blog_type import Blog



class BlogManager:
    def __init__(self, dataBase: MongoDBManager):
        self.db = dataBase

    def add_blog(self, blog: Blog) -> str:
        """
        添加一个博客,返回生成的唯一ID。

        Args:
            blog (Blog): 博客对象

        Returns:
            str: 插入后的文档的 ID
        """
        return self.db.insert_one("blogs", blog.model_dump())

    def delete_blog(self, blog_id: str) -> bool:
        """
        删除指定ID的博客。

        Args:
            blog_id (str): 博客的 ID

        Returns:
            bool: 删除成功返回 True，否则返回 False
        """
        result = self.db.delete_one("blogs", {"_id": ObjectId(blog_id)})
        return result.deleted_count > 0

    def get_blog(self, blog_id: str) -> Blog:
        """
        获取指定ID的博客。

        Args:
            blog_id (str): 博客的 ID

        Returns:
            Blog: 博客对象，如果不存在则返回 None
        """
        blog_data = self.db.find_one("blogs", {"id": blog_id})
        if blog_data:
            return Blog(**blog_data)
        return None