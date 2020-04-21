#-*- coding:utf-8 -*-

import unittest

from session import UserSessionRedis


class TestServerRedis(unittest.TestCase):
    """ test session redis
        """
    def setUp(self):
        self.r = UserSessionRedis()
        self.r.initialize()

    def test_set_connection(self):
        self.assertEqual(self.r.connection.set('PING', 'PONG'), True)

    def test_get_connection(self):
        self.assertEqual(self.r.connection.get('PING'), b'PONG')

    def test_add(self):
        self.assertEqual(self.r.add(123456789, dict(PING='PONG')), None)

    def test_get(self):
        self.assertEqual(self.r.get(123456789), {b'PING': b'PONG'})
