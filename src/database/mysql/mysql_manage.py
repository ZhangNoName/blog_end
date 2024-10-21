import pymysql

class MySQLManager:
    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def execute(self, sql, params=None):
        """执行 SQL 语句"""
        self.cursor.execute(sql, params)
        self.conn.commit()

    def fetchone(self, sql, params=None):
        """获取一条结果"""
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def fetchall(self, sql, params=None):
        """获取所有结果"""
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def close(self):
        """关闭数据库连接"""
        self.cursor.close()
        self.conn.close()