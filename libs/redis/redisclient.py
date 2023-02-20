# -*- coding:utf-8 -*-
from libs.redis.redisclus import RedisClus
from libs.redis.redispool import RedisPool


class RedisClient(object):
	"""docstring for RedisClus"""
	def __init__(self, config, env):
		super(RedisClient, self).__init__()
		self.config = config
		self.env = env
		self.client = None

	def get_client(self):
		redis_config = self.config['redis-' + self.env]
		if self.env.find("pool") != -1:
			# redis 连接池
			redispool = RedisPool(redis_config)
			self.client = redispool.get_client()
		else:
			# 集群
			redisclus = RedisClus(redis_config)
			self.client = redisclus.get_client()
		return self.client

