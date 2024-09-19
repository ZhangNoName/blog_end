import os
import uuid
from typing import Dict, Type, Union, List

import yaml
from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from loguru import logger
from pydantic import BaseModel
from fastapi import UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

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
        self.load_config(env=env)  # todo: modify env config
        self.__init__mongoDB()
        self.__init__redis()
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
        """初始化链接到mongoDB"""
        self.mongo = MongoDBManager(ip=self.config['mongo']['ip'],port=self.config['mongo']['port'],db=self.config['mongo']['db'],user=self.config['mongo']['user'],passwd=self.config['mongo']['passwd'])
        
        
    def __init__redis(self):
        """
        初始化redis类
        """
        self.redis = RedisManager(ip=self.config['redis']['ip'],port=self.config['redis']['port'],db=self.config['redis']['db'],auth=self.config['redis']['auth'],key_prefix='blog')
        
    def __init_memory_by_file(self):
        pass

    def __init_conversation_by_file(self):
        pass



@asynccontextmanager
async def lifespan(app: Application):
    env = os.getenv('ENV', 'local')
    app.init(env)
    logger.debug('start up event')
    yield
    app.shut_down()
    logger.debug('stop event')


app = Application(lifespan=lifespan)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")