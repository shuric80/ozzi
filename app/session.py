#-*- coding:utf-8 -*-
from shortuuid import uuid
from log import logger

class Session:
    """
     Class singleton for cookie-session on server.
      """

    def __init__(self):
        logger.info('Session object created.')
        logger.info('')
        self._d = dict()

    @property
    def id(self):
        id = uuid()
p       self._d[id] = dict()
        return id


    def add(self,id, d_input):
        #if isinstance(d_input, dict) and isinstance(id, str):
        logger.debug('Session add: {id} : {data}'.format(id=id, data=d_input))
        if id not in self._d:
            logger.error('Session ID unavailable')
            return

        self._d[id] = d_input

    def get(self, id):
        return self._d.get(id)

    def __repr__(self):
        return '<>'.format(self._d)


cookie_session = Session()
