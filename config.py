# -*- coding:utf-8 -*-
CNT = 10
SESSION_TIME = 3600
SECRET_COD = 'kuku'
WEBHOOK_SSL_CERT = 'webhook_cert.pem'
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'
WEBHOOK_HOST = '62.109.13.25'
WEBHOOK_PORT = 443
WEBHOOK_URL_BASE = 'https://{!s}:{}'.format(WEBHOOK_HOST, WEBHOOK_PORT)
#TOKEN = '246271863:AAEUJQJ7aHByov0wnHBjSUGseL1ixU1mSgk'
TOKEN = '163963654:AAGaVG5vMSfZ5nuGV9q5FyGcojW-ShoJR0k'
VK_TOKEN = '54cbe13354cbe13354cbe1334054975dd8554cb54cbe1330d8ffa0ce43119178d2f7ead'
DEBUG = True
TESTING = True
CELERY_BROKER_URL  = 'redis://localhost:6379/0'
#DATABASE = 'bot.db'
GROUPS = (
    {
        'name':'2mambo',
        'url':'2mamboproject',
    },
    {
        'name':'salsa jem',
        'url':'salsa_jam'
    },
    {
        'name':'',
        'url':'salsann'
    },
    {
        'name':'',
        'url':'svoyashkola'
    },
    {
        'name':'',
        'url':'armenycasa'
    },
    {
        'name':'',
        'url':'maleconmoscow'
    },
    {
        'name':'',
        'url':'sensualbachatakizombanight'
    },
    {
        'name':'',
        'url':'mambo.love'
    },
    {
        'name':'',
        'url':'fair_dance'
    }


)

#TODO add text for help
HELP = """
Бот умеет:
  /list - список всех групп.
  /settings - настройка индивидуального фильтра новостей.
  /last — 5 последних новостей. Если в /settings ничего не настраивали, то выдаст по всем группам.
  /last N — (N- число от 1 до 9)  последних новостей.
"""
