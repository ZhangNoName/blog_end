from datetime import datetime
from typing import Optional
from loguru import logger
from src.database.mysql.mysql_manage import MySQLManager
from src.type.user_type import User

class UserManager:
    table_name = "user"
    all_attr = "id, user_name, name, age, phone, email, passwd, birth_day, create_time"
    def __init__(self, db:MySQLManager):
        self.db = db

    def create_user(self, user:User):
        """
        创建用户

        Args:
            name (str): 用户名
            age (int): 年龄
            phone (str): 手机号码
            email (str): 邮箱
            passwd (str): 密码
            birth_day (str): 生日，格式为YYYY-MM-DD
        """
        sql = f"INSERT INTO {self.table_name} (user_name, name, age, phone, email, passwd, birth_day, create_time) VALUES (%s,%s,%s, %s, %s, %s, %s,  NOW())"
        val = (user.user_name,user.name, user.age, user.phone, user.email, user.passwd, user.birth_day)
        try:
            # self.db.execute(sql, [val])
            res = self.db.execute(sql,val)
            logger.info(f"用户创建成功{res}")
            return True
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return False


    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        根据用户ID查询用户信息

        Args:
            user_id (int): 用户ID

        Returns:
            User: User对象，如果不存在则返回None
        """
        sql = f"SELECT {self.all_attr} FROM {self.table_name} WHERE id = %s"
        result = self.db.fetch_one(sql, user_id)
        logger.info(f"根据id查询的结果{result}")
        
        # 查询结果是字典形式
        if isinstance(result, dict):
            user_data = result
        else:
            # 如果是元组形式，手动构造字典
            user_data = dict(zip(self.all_attr.split(', '), result))
        return user_data
    def get_user_by_name(self, name: str, page: int = 1, per_page: int = 10) -> list[User]:
        """
        根据用户名模糊查询用户信息，支持分页

        Args:
            name (str): 用户名
            page (int): 页码，从1开始，默认为1
            per_page (int): 每页显示的记录数量，默认为10

        Returns:
            list[User]: 查询到的用户列表
        """
        offset = (page - 1) * per_page
        sql = f"""
        SELECT {self.all_attr} 
        FROM {self.table_name} 
        WHERE name LIKE %s 
        ORDER BY id ASC 
        LIMIT %s OFFSET %s
        """
        # 将参数打包为一个元组
        params = (f"%{name}%", per_page, offset)

        # 传递参数时使用元组
        result = self.db.execute(sql, params)

        # 将查询结果转换为User对象列表
        users = [User(**dict(zip(self.all_attr.split(', '), row))) for row in result]
        return users


    # 其他查询方法，如根据name、phone查询，类似于get_user_by_id

    def update_user(self, id:str, **kwargs):
        """
        更新用户信息

        Args:
            id (int): 用户ID
            kwargs: 要更新的字段和值，例如：name='new_name', age=30
        """
        # 构造更新语句
        set_clause = ', '.join(f"{key} = %s" for key in kwargs)
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
        # 构造参数
        values = tuple(kwargs.values()) + (id,)
        self.db.execute(sql, values)

    def delete_user(self, id:str):
        """
        删除用户

        Args:
            id (int): 用户ID
        """
        sql = "DELETE FROM users WHERE id = %s"
        val = (id,)
        self.db.execute(sql, val)