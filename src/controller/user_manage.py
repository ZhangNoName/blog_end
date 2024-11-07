from datetime import datetime
from loguru import logger
from src.database.mysql.mysql_manage import MySQLManager
from src.type.user_type import User

class UserManager:
    table_name = "user"
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
        sql = f"INSERT INTO {self.table_name} (id,name, age, phone, email, passwd, birth_day, create_time) VALUES (%s,%s, %s, %s, %s, %s, %s, NOW())"
        val = (user.id,user.name, user.age, user.phone, user.email, user.passwd, user.birth_day)
        sql = f"INSERT INTO {self.table_name} (name, age, phone, email, passwd, birth_day, create_time) VALUES ('zxy', 18, '17683242528', '123456@qq.com', '123456', '1998-05-28', NOW())"

        logger.info('当前执行的sql:',sql)
        try:
            # self.db.execute(sql, [val])
            res = self.db.execute(sql)
            logger.info(f"用户创建成功{res}")
            return True
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return False


    def get_user_by_id(self, id:str):
        """
        根据用户ID查询用户信息

        Args:
            id (int): 用户ID

        Returns:
            tuple: 用户信息元组，如果不存在则返回None
        """
        sql = f"SELECT * FROM {self.table_name} WHERE id = %s"
        val = (id,)
        self.db.execute(sql, val)
        result = self.db.cursor.fetchone()
        return result
    def get_user_by_name(self, name:str):
        """
        根据用户ID查询用户信息

        Args:
            name (str): 用户ID

        Returns:
            tuple: 用户信息元组，如果不存在则返回None
        """
        sql = f"SELECT * FROM {self.table_name} WHERE id = %s"
        val = (name,)
        self.db.execute(sql, val)
        result = self.db.cursor.fetchone()
        return result

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