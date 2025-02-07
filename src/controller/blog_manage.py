from typing import List
import uuid
from datetime import datetime

from bson import ObjectId
from loguru import logger
from pymongo.cursor import Cursor
from src.database.mongo.mongodb_manage import MongoDBManager
from src.database.mysql.mysql_manage import MySQLManager
from src.type.blog_type import Blog, BlogBase



class BlogManager:
    def __init__(self,baseDB:MySQLManager, contentDB: MongoDBManager):
        self.db = baseDB
        self.contentDB = contentDB

    def add_blog(self, blog: Blog) -> str:
        """
        添加一个博客,返回生成的唯一ID。

        Args:
            blog (Blog): 博客对象

        Returns:
            str: 插入后的文档的 ID
        """
        # return self.contentDB.insert_one("blogs", blog.model_dump())
        
        sql = """
        INSERT INTO blog_base ( title, author,  updated_at, abstract, is_deleted)
        VALUES ( %s, %s, %s, %s, %s)
        """
        logger.info(f'插入的数据{blog}')
        params = ( blog.title, blog.author,  blog.updated_at, blog.abstract, 0)
        self.db.execute(sql, params)

        # 插入MongoDB记录
        return self.contentDB.insert_one("blogs", {"blogId": blog.id, "title": blog.title, "content": blog.content})

    def delete_blog(self, blog_id: str) -> bool:
        """
        删除指定ID的博客。

        Args:
            blog_id (str): 博客的 ID

        Returns:
            bool: 删除成功返回 True，否则返回 False
        """
        sql = """
        UPDATE blogs
        SET is_deleted = TRUE
        WHERE id = %s AND is_deleted = FALSE
        """
        result = self.db.execute(sql, (blog_id,))
        return result > 0

    def get_blog(self, blog_id: str) -> Blog:
        """
        获取指定ID的博客。

        Args:
            blog_id (str): 博客的 ID

        Returns:
            Blog: 博客对象，如果不存在则返回 None
        """
        blog_data = self.contentDB.find_one("blogs", {"id": blog_id})
        logger.info(f'查询到的结果{blog_data}')
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
        blogs_data = self.db.find_page_query("blog_base", filter={}, skip=skip, page_size=page_size)
        # total_count = self.db.find_count("blogs")
        total_count = 10
        # 将查询出来的字典数据转换为 Blog 对象
        blogs = [BlogBase(**blog_data) for blog_data in blogs_data]
        return {
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "list": blogs
            # "list": blogs_data
        }
        # 查询MySQL数据库，排除已删除的博客
        sql = """
        SELECT id, title, author, updated_at, abstract,view_count,comment_count,tag,category,byte_num
        FROM blog_base
        WHERE is_deleted = 0
        LIMIT %s OFFSET %s
        """
        blogs_data = self.db.execute(sql, (page_size, skip))

        # 获取总记录数
        total_count = self.db.execute("SELECT COUNT(*) FROM blog_base WHERE is_deleted = FALSE", ())

        return {
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "list": [Blog(**blog_data) for blog_data in blogs_data]
        }