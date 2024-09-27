from typing import List
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
    
    def get_blog_by_page(self, page: int, page_size: int) -> List[Blog]:
        """
        分页获取博客列表。

        Args:
            page (int): 页码，从1开始
            page_size (int): 每页显示的博客数量

        Returns:
            List[Blog]: 分页后的博客列表
        """

        skip = (page - 1) * page_size
        blogs_data = self.db.find_page_query("blogs", filter={}, skip=skip, page_size=page_size)
        total_count = self.db.find_count("blogs")

        return {
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "list": [Blog(**blog_data) for blog_data in blogs_data]
        }