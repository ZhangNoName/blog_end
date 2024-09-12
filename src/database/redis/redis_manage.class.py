import json
from loguru import logger
import redis
from typing import Any, Dict, Optional, Union

class RedisManager:
    """
    Redis 管理类，用于执行增、删、查、改操作
    """

    def __init__(self, host: str, port: int, db: int, auth: str):
        """
        初始化 Redis 连接

        Args:
            host (str): Redis 服务器地址
            port (int): Redis 服务器端口
            db (int): Redis 数据库编号
            key_prefix (str): 键前缀
            auth (str): Redis 认证密码
        """
        try:
            self.client = redis.StrictRedis(host=host, port=port, db=db, password=auth, decode_responses=True)
        except redis.RedisError as e:
            logger.error(f"Redis connection error: {e}")

    def set_item(self, key: str, value: Union[str, dict], prefix: str, expire: Optional[int] = None) -> bool:
        """
        设置键值对

        Args:
            key (str): 键
            value (Union[str, dict]): 值，可以是字符串或字典等
            prefix (str): 键前缀
            expire (Optional[int]): 过期时间（秒），默认不过期

        Returns:
            bool: 操作是否成功
        """
        full_key = prefix + key
        if isinstance(value, dict):
            value = json.dumps(value)  # 将字典转换为 JSON 字符串
        try:
            if expire:
                return self.client.set(full_key, value, ex=expire)
            return self.client.set(full_key, value)
        except redis.RedisError as e:
            logger.error(f"Redis set error: {e}")
            return False

    def get_item(self, key: Optional[str] = None, prefix: Optional[str] = None) -> Union[Optional[str], Dict[str, str]]:
        """
        获取指定键的值或所有带前缀的键值对

        Args:
            key (Optional[str]): 键
            prefix (Optional[str]): 键前缀

        Returns:
            Union[Optional[str], Dict[str, str]]: 键对应的值，如果键不存在则返回 None；如果不传入键，则返回所有带前缀的键值对
        """
        try:
            if key:
                full_key = prefix + key
                value = self.client.get(full_key)
                try:
                    return json.loads(value)  # 尝试将 JSON 字符串转换回字典
                except (TypeError, json.JSONDecodeError):
                    return value  # 如果转换失败，返回原始值
            else:
                cursor = '0'
                result = {}
                prefix_length = len(prefix)
                while cursor != 0:
                    cursor, keys = self.client.scan(cursor=cursor, match=prefix + '*')
                    for key in keys:
                        clean_key = key[prefix_length:]  # 去掉前缀
                        value = self.client.get(key)
                        try:
                            result[clean_key] = json.loads(value)  # 尝试将 JSON 字符串转换回字典
                        except (TypeError, json.JSONDecodeError):
                            result[clean_key] = value  # 如果转换失败，返回原始值
                return result
        except redis.RedisError as e:
            logger.error(f"Redis get error: {e}")
            return None

    def delete_item(self, key: str, prefix: str) -> bool:
        """
        删除指定键

        Args:
            key (str): 键
            prefix (str): 键前缀

        Returns:
            bool: 操作是否成功
        """
        full_key = prefix + key
        try:
            return self.client.delete(full_key) == 1
        except redis.RedisError as e:
            logger.error(f"Redis delete error: {e}")
            return False

    def update_item(self, key: str, value: Union[str, dict], prefix: str, expire: Optional[int] = None) -> bool:
        """
        更新指定键的值

        Args:
            key (str): 键
            value (Union[str, dict]): 新值
            prefix (str): 键前缀
            expire (Optional[int]): 过期时间（秒），默认不过期

        Returns:
            bool: 操作是否成功
        """
        full_key = prefix + key
        try:
            if self.client.exists(full_key):
                if isinstance(value, dict):
                    value = json.dumps(value)  # 将字典转换为 JSON 字符串
                if expire:
                    return self.client.set(full_key, value, ex=expire)
                return self.client.set(full_key, value)
            return False
        except redis.RedisError as e:
            logger.error(f"Redis update error: {e}")
            return False
    