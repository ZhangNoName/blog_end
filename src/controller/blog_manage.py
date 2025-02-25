from typing import List, Union
import uuid
from datetime import datetime

from bson import ObjectId
from loguru import logger
from pymongo.cursor import Cursor
from src.database.mongo.mongodb_manage import MongoDBManager
from src.database.mysql.mysql_manage import MySQLManager
from src.type.blog_type import Blog, BlogBase, BlogCreate, TagNew



class BlogManager:
    def __init__(self,baseDB:MySQLManager, contentDB: MongoDBManager):
        self.db = baseDB
        self.contentDB = contentDB

    def get_or_create_tag(self, tag: Union[str, TagNew],blog_id:str) -> int:
        """检查标签是否存在，不存在则创建"""

        if isinstance(tag, str):
            # 已有标签，直接返回 ID
            logger.info('已有id',tag)
            id =  tag
        elif isinstance(tag, TagNew):
            # 查询是否存在该标签
            tag_name = tag.name.strip() 
            sql = "SELECT id FROM tag WHERE name = %s"
            id = self.db.fetch_one(sql, tag_name)
            if id is None:
                create_sql = """
                    INSERT INTO tag (name) VALUES (%s)
                """
                # 不存在，插入新标签
                id = self.db.execute(create_sql, tag_name)
        # 插入博客标签关联表
        if id:
            # 插入 blog_tag 关系表
            blog_tag_sql = "INSERT IGNORE INTO blog_tag (blog_id, tag_id) VALUES (%s, %s)"
            self.db.execute(blog_tag_sql, (blog_id, id))
        return id
            
        
    def add_blog(self, blog: BlogCreate) -> str:
        """
        添加一个博客,返回生成的唯一ID。

        Args:
            blog (Blog): 博客对象

        Returns:
            str: 插入后的文档的 ID
        """
        # return self.contentDB.insert_one("blogs", blog.model_dump())
        
        sql = """
        INSERT INTO blog (title, author, abstract,  category, updated_at, is_deleted)
        VALUES (%s, %s,  %s, %s, NOW(), 0)
        """
        params = (blog.title, blog.author, blog.abstract,  blog.category)
        id = self.db.execute(sql, params) 
        # logger.info(f'插入的结果{res}')
         # 处理标签，确保所有 tag 都是 ID
        tag_ids = [self.get_or_create_tag(tag,id) for tag in blog.tag]
        # 将内容插入MongoDB记录
        result = self.contentDB.insert_one("blogs", {"blogId": id, "title": blog.title, "content": blog.content})
        if result:
            return id
        return None

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

    def get_blog(self, blog_id:int) -> Blog:
        """
        获取指定ID的博客。

        Args:
            blog_id (str): 博客的 ID

        Returns:
            Blog: 博客对象，如果不存在则返回 None
        """
        blog_data = self.contentDB.find_one("blogs", {"blogId": blog_id})
        logger.info(f'查询到的结果{blog_id}{blog_data}')
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
        blogs_data = self.db.find_page_query("blog", filter={}, skip=skip, page_size=page_size)
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
        FROM blog
        WHERE is_deleted = 0
        LIMIT %s OFFSET %s
        """
        blogs_data = self.db.execute(sql, (page_size, skip))

        # 获取总记录数
        total_count = self.db.execute("SELECT COUNT(*) FROM blog WHERE is_deleted = FALSE", ())

        return {
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "list": [Blog(**blog_data) for blog_data in blogs_data]
        }