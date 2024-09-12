from typing import Optional
from pymongo import MongoClient
import gridfs
import numpy as np
from loguru import logger

class MongoDBManager:
    def __init__(self, db_name:str, host:str, port:str, user:str, passWord:str):
        uri = f"mongodb://{user}:{passWord}@{host}:{port}/{db_name}?authSource=admin"
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.fs = gridfs.GridFS(self.db)
            self.host = host
            self.port = port
            self.db_name = db_name
            self.user = user
            self.passWord = passWord
            logger.info("MongoDB connection established.")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")

    def open_connection(self):
        """
        链接到一个数据库
        """
        try:
            self.client = MongoClient(self.host, self.port)
            self.db = self.client[self.db_name]
            self.fs = gridfs.GridFS(self.db)
            logger.info("Database connection opened.")
        except Exception as e:
            logger.error(f"Error opening database connection: {e}")

    def close_connection(self):
        """
        断开与数据库的链接
        """
        try:
            self.client.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
    
    def delete(self, query, collection_name=None):
        """
        删除满足查询条件的数据。

        Parameters:
            query (dict): 查询条件，用于匹配要删除的文档。
            collection_name (str, optional): 集合名称。如果未指定，则使用默认集合名称。

        Returns:
            dict: 包含删除操作结果的对象。
        """
        try:
            if collection_name is None:
                logger.error('未传入要删除的集合名称')
                return False

            collection = self.db[collection_name]
            result = collection.delete_one(query)

            if result.deleted_count > 0:
                logger.info(f"Deleted {result.deleted_count} document(s) from {collection_name}.")
            else:
                logger.info(f"No matching documents found in {collection_name} to delete.")

            return {"deleted_count": result.deleted_count}
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return None
    
   
    def find_collection(self, collection_name):
        """
        查找集合内全部数据
        
        Args:
            collection_name[str]:集合的名称
        """
        try:
            collection = self.db[collection_name]
            result = collection.find()
            if result:
                logger.info(f"Found data in {collection_name}.")
                return result
            else:
                logger.info(f"No matching data found in {collection_name}.")
                return None
        except Exception as e:
            logger.error(f"Error finding data in {collection_name}: {e}")
            return None
