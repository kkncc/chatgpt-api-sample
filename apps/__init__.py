# -*- coding:utf-8 -*-
import configparser
import logging
import os
import json
import sys

from flask import Flask, request, abort
# flask环境配置
from libs.common import pub
from libs.redis.redisclient import RedisClient
from setting import APP_ROOT
from loguru import logger

logger.add(sys.stderr, level="INFO", format="[{level} {time:YYYY-MM-DD HH:mm:ss}] {message}")

GLOBAl_CONFIG = configparser.ConfigParser()
GLOBAl_CONFIG.read(APP_ROOT + '/config/conf.ini')

PROJECT_ENV = GLOBAl_CONFIG['main']['env']

# os.environ['dev'] = APP_ROOT + '/config/dev-conf.ini'
# os.environ['uat'] = APP_ROOT + '/config/uat-conf.ini'
os.environ['prod'] = APP_ROOT + '/config/prod-conf.ini'

app = Flask(__name__, static_folder='../static')
app.config.from_envvar(PROJECT_ENV)
# 日志级别
app.logger.setLevel(logging.DEBUG)

# 是否开启uat
UAT_CONFIG = configparser.ConfigParser()

app.config['MAX_CONTENT_LENGTH'] = 2048 * 1024 * 1024

redis_model = app.config.get("REDIS_MODEL")

redis_setting = RedisClient(GLOBAl_CONFIG, redis_model + "-" + PROJECT_ENV)
GLOBAL_REDIS_CLIENT = redis_setting.get_client()
MISSING_PARAMETERS = {'code': 2000, 'msg': 'missing parameters'}
ACCESS_DENIED = {'code': 3001, 'msg': 'access denied'}
DEFAULT_OK = {'code': 0, 'msg': 'success'}

from .v1 import v1 as v1_blueprint
app.register_blueprint(v1_blueprint)


trusted_proxies = ('127.0.0.1', "192.168.1.0")


@app.before_request
def before_request():
    # 本地开发环境，ip访问限制
    if PROJECT_ENV != 'prod':
        remote = request.remote_addr
        while remote not in trusted_proxies:
            abort(403)


@app.after_request
def after_request(resp):
    """ 每一次请求之后被调用

    :param resp:    这个参数是response对象
    :return:    需要返回一个response对象，可以是新的，也可以是传入进入的
    """
    if request.path.find("api") != -1:
        ip = pub.get_ip_addr(request)
        data = resp.get_json()
        # 是否有数据返回, 过滤文件流的数据
        if data:
            logger_info = {
                "response func": request.path,
                "ip": ip,
                "data": json.dumps(data)
            }
            logger_info = pub.merge_log_info(logger_info)
            logger.info(json.dumps(logger_info))
    return resp

