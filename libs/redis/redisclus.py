# -*- coding:utf-8 -*-
from rediscluster import StrictRedisCluster


class RedisClus(object):
	"""docstring for RedisClus"""
	def __init__(self, arg):
		super(RedisClus, self).__init__()
		self.arg = arg
		self.redis_nodes = []
		for x in self.arg:
			if not x.startswith('port'):
				continue
			nodes = {
				'host': self.arg[x],
				'port': int(x.replace("port", ""))
			}
			self.redis_nodes.append(nodes)
		self.client = None

	def get_client(self):
		if not self.client:
			try:
				self.client = StrictRedisCluster(
					startup_nodes=self.redis_nodes,
					password=self.arg.get('password'),
					decode_responses=True
				)
			except Exception as e:
				print("connect error", e)
		return self.client
