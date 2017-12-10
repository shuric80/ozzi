#-*- coding:utf-8 -*-
import shortuuid
import json
import redis
from log import logger

class UserSessionRedis:
    """
     Class singleton for cookie-session on server.
      """

    __slots__ = ['connection', 'id']

    def __init__(self, id = None):
        logger.info('Session object created.')
        self.connection = None
        self.id = shortuuid.uuid() if not id else id
        self.initialize()

    def initialize(self):
        self.connection = redis.StrictRedis(host='localhost', port =6379, db =0)

    def add(self, d_input):
        self.connection.hmset(self.id, d_input)

    def get(self, id):
        return self.connection.hgetall(id)
