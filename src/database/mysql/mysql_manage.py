import pymysql
import time

class MySQLManager:
    """
    MySQL连接监控类，基于PyMySQL库实现。

    该类提供了一个健壮的MySQL连接，自动重连、错误处理等功能。

    属性:
        ip (str): MySQL服务器主机名
        port (str): MySQL服务器端口
        user (str): MySQL用户名
        password (str): MySQL密码
        database (str): MySQL数据库名
        charset (str, optional): 字符集，默认为utf8mb4
        max_retry_times (int, optional): 最大重试次数，默认为3
        retry_interval (int, optional): 重试间隔时间（秒），默认为5

    方法:
        __init__: 初始化连接
        connect: 建立连接
        is_alive: 检查连接是否存活
        reconnect: 重连
        execute: 执行SQL语句
    """

    def __init__(self, ip,port,db,  user=None, passwd=None, charset='utf8mb4', max_retry_times=3, retry_interval=5):
        """初始化连接"""
        self.host = ip
        self.port = port
        self.user = user
        self.password = passwd
        self.database = db
        self.charset = charset
        self.max_retry_times = max_retry_times
        self.retry_interval = retry_interval
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        """建立连接"""
        try:
            self.cnx = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset
            )
            self.cursor = self.cnx.cursor()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 连接MySQL数据库成功！")
        except pymysql.Error as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 连接MySQL数据库失败：{e}")

    def is_alive(self):
        """检查连接是否存活"""
        try:
            self.cursor.execute("SELECT 1")
            return True
        except pymysql.Error:
            return False

    def reconnect(self):
        """重连"""
        for i in range(self.max_retry_times):
            self.connect()
            if self.is_alive():
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 重连MySQL数据库成功！")
                return
            time.sleep(self.retry_interval)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 重试{self.max_retry_times}次后，仍无法连接MySQL数据库！")

    def execute(self, sql, *args):
        """执行SQL语句

        Args:
            sql (str): 要执行的SQL语句
            *args: 可变参数，用于绑定SQL语句中的参数

        """
        if not self.is_alive():
            self.reconnect()
        try:
            self.cursor.execute(sql, args)
            self.cnx.commit()
        except pymysql.Error as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 执行SQL语句失败：{e}")