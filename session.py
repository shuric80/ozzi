#-*- coding:utf-8 -*-
import logging

class SessionBuffer:
    
    def __init__(self ):
        self._session = dict()

    def add(self, id, tag, page = None):
        self._session[id] = dict(tag=tag, page=page)
        logging.info('Add session: id= %s \nSize session buffer: %s' % (id, len(self._session)))

    def cmd(self, id, command):
        
        if not self._session.has_key(id):
            logging.error('Not found session')
            return None
            
        self._session[id]['page'] = _cnt

        if command == 'next':
            _cnt += 1 if self.cnt <10 else 0

        elif command == 'back':
            _cnt -= 1 if self.cnt > 0 else 0

        self._session[id]['page'] = _cnt

        tag = self._session[id]['tag']
        page = self._session[id]['page']
        return tag
