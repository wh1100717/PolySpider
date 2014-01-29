#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import redis
from PolySpider.config import Config

REDIS = Config.REDIS
pool = redis.ConnectionPool(host=REDIS['host'],password=REDIS['password'], port=REDIS['port'],db=REDIS['db'])


class RedisClient(object):
	def __init__(self):
		self.redis_client = redis.Redis(connection_pool = pool)

	'''
	Key-value操作:
		get(key): 获取对应的value
		set(key,value): set对应key的value
		delete(key): 删除key及对应的value
		incr(key,amount): value自增amount相对应的量
	'''
	def get(self,redis_name):
		return self.redis_client.get(redis_name)

	def set(self,redis_name,redis_value):
		return self.redis_client.set(redis_name, redis_value)

	def delete(self,redis_name):
		code = self.redis_client.delete(redis_name)
		return True if code else False

	def incr(self,redis_name, amount = 1):
		return self.redis_client.incr(redis_name,amount)

	'''
	List操作:
		push_item(key,value1,value2,...): 从列表末尾推入项
		lpush_item(key,value1,value2,...): 从队列头退入项
		push_list(key,list): 合并队列，新List自动添加到末尾
		lpush_list(key,list): 合并队列，新List自动添加到列头
		pop_item(key): 从队列末尾推出项
		lpop_item(key): 从队列头推出项
		get_items(key,start,end,redis_type): 获取队列中的项
		get_length(key): 获取队列的长度
	'''
	def push_item(self,redis_name,*redis_values):
		return self.redis_client.rpush(redis_name,*redis_value)

	def lpush_item(self,redis_name,*redis_values):
		return self.redis_client.lpush(redis_name,*redis_value)

	def push_list(self,redis_name,redis_list):
		return self.redis_client.rpush(redis_name,*redis_list)

	def lpush_list(self,redis_name,redis_list):
		return self.redis_client.lpush(redis_name,*redis_list)

	def pop_item(self,redis_name):
		return self.redis_client.rpop(redis_name)

	def lpop_item(self,redis_name):
		return self.redis_client.lpop(redis_name)
		
	def get_items(self,redis_name,start,end, redis_type = 'list'):
		'''
		redis_type
			list: 返回数组的items
			sorted_set: 返回有序set的items
		'''
		if redis_type == 'list':
			return self.redis_client.lrange(redis_name,start,end)
                elif redis_type == 'sorted_set':
			return self.redis_client.zrange(redis_name,start,end)
	def get_length(self,redis_name):
		return self.redis_client.llen(redis_name)

	'''
	Set操作:

	'''
	def sset(redis_name, *redis_members):
		return self.redis_client.sadd(redis_name,redis_members)

	def soreted_sset(redis_name, *args, **kwargs):
		'''
		输入格式为
			1. redis_name, redis_index1(float), redis_member1, redis_index2, redis_member2....
			2. redis_name, redis_member1 = redis_index1, redis_member2 = redis_index2....
		'''
		if args and len(args) % 2 != 0:
			return False
		for key in kwargs:
			args.append(kwargs[key])
			args.append(key)
		return self.redis_client.zadd(redis_name,*args)

	def sdelete(redis_name,redis_member):
		return self.redis_client.srem(redis_name,redis_member)

	def spop(redis_name):
		return self.redis_client.spop(redis_name)

	def sexist(redis_name, redis_member):
		return self.redis_client.sismember(redis_name,redis_member)

	def sget_all(redis_name):
		return self.redis_client.smembers(redis_name)

	def union_set(redis_name_1, redis_name_2):
		return self.redis_client.sunion(redis_name_1,redis_name_2)

	'''
	Hashes(可以理解成map或者字典)操作:
	'''
	def hset(redis_name, *args, **kwargs):
		'''
		输入格式为:
			1. redis_name, redis_key1, redis_value1, redis_key2, redis_value2....
			2. redis_name, redis_key1 = redis_value1, redis_key2 = redis_value2....
		'''
                print args
		if args and len(args) % 2 != 0:
			return False
		for pair in kwargs:
			args.append(key)
			args.append(kwargs[key])
                print '!!!!!!!!!!!!!!!!!!!!'
                print args
                print '!!!!!!!!!!!!!!!!!!!!!'
                pipe = self.redis_client.pipeline()
		for i in range(len(args)/2):
			pipe.hset(redis_name,args[2*i],args[2*i+1])
		code = pipe.execute()
		return True if code else False

	def hset_map(redis_name, dictionary):
		pipe = self.redis_client.pipeline()
		for key in dictionary:
			pipe.hset(redis_name,key,dictionary[key])
		code = pipe.execute()
		return True if code else False

	def hget(redis_name, redis_key):
		return self.redis_client.hget(redis_name,redis_key)

	def hget_all(redis_name):
		return self.redis_client.hgetall(redis_name)

	def hincr(redis_name, redis_key, amount = 1):
		return self.redis_client.hincyby(redis_name,redis_key,amount)

	def hdel(redis_name, *redis_keys):
		return self.redis_client.hdel(redis_name,*redis_keys)





	


