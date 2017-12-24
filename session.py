#-*- coding:utf-8 -*-
import shortuuid
import json
import redis
from log import logger
import config

class UserSessionRedis:
    """
     Class singleton for cookie-session on server.
      """

    __slots__ = ['connection']

    def __init__(self):
        logger.info('Session object created.')
        self.connection = None
        self.initialize()

    @property
    def id(self):
        return shortuuid.uuid()

    def initialize(self):
        self.connection = redis.StrictRedis(host='localhost', port =6379, db =0)

    def add(self, id, d_input):
        logger.debug('ADD:{} {}'.format(id, d_input))
        self.connection.hmset(id, d_input)

    def get(self, id):
        logger.debug('GET:{}'.format(id))
        d = self.connection.hgetall(id)
        return dict((k.decode('utf-8'), v.decode('utf-8')) for k,v in d.items())
