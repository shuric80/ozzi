#-*- coding:utf-8 -*-

from log import logger

class Session:
    """
     Class singleton for cookie-session on server.
      """

    def __init__(self):
        logger.info('Session object created.')
        self._d = dict()

    @property
    def id(self):
        return uuid()

    def add(self,id, d_input):
        #if isinstance(d_input, dict) and isinstance(id, str):
        logger.debug('Session add: {id} : {data}'.format(id=id, data=d_input))
        self._d[id] = d_input

    def get(self, id):
        return self._d.get(id)

    def __repr__(self):
        return '<>'.format(self._d)


cookie_session = Session()
