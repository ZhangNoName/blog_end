# app_instance.py
import os
import yaml
from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from src.controller.blog_manage import BlogManager
from src.database.mongo.mongodb_manage import MongoDBManager
from src.database.redis.redis_manage import RedisManager

class Application(FastAPI):
    def __init__(self, **args):
        super(Application, self).__init__(**args)
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def init(self, env='dev'):
        self.load_config(env=env)
        self.__init__mongoDB()
        self.__init__redis()
        self.__init_blog_manager()
        logger.info(f'当前模式为{env}')
        if env == 'local':
            pass
        else:
            pass

    def shut_down(self, env='dev'):
        if env == 'local':   
            pass
        else:
           pass

    def load_config(self, env='dev'):
        config_path = f'./src/conf/{env}.yml'

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        logger.info(f'{env}环境的配置{self.config}')
        logger.debug(f'Loaded configuration for environment: {env}')

    def __init__mongoDB(self):
        self.mongo = MongoDBManager(ip=self.config['mongo']['ip'], port=self.config['mongo']['port'], db=self.config['mongo']['db'], user=self.config['mongo']['user'], passwd=self.config['mongo']['passwd'])

    def __init__redis(self):
        self.redis = RedisManager(ip=self.config['redis']['ip'], port=self.config['redis']['port'], db=self.config['redis']['db'], auth=self.config['redis']['auth'], key_prefix='blog')

    def __init_blog_manager(self):
        self.blog = BlogManager(dataBase=self.mongo)
        

@asynccontextmanager
async def lifespan(app: Application):
    env = os.getenv('ENV', 'local')
    app.init(env)
    logger.debug('start up event')
    yield
    app.shut_down()
    logger.debug('stop event')

app = Application(lifespan=lifespan)
