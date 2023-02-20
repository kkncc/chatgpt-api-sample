# -*- coding:utf-8 -*-
import redis


class RedisPool(object):
	"""docstring for RedisPool"""
	def __init__(self, arg):
		super(RedisPool, self).__init__()
		# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
		self.pool = redis.ConnectionPool(host=arg["host"], port=arg['port'], password=arg.get("password"), decode_responses=True)
		self.client = None

	def get_client(self):
		if not self.client:
			self.client = redis.Redis(connection_pool=self.pool)
		return self.client
