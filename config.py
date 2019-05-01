# -*- coding:utf-8 -*-
import os
CNT = 10
SESSION_TIME = 3600
SECRET_COD = 'kuku'
WEBHOOK_SSL_CERT = 'webhook_cert.pem'
WEBHOOK_SSL_PRIV = 'webhook_pkey.pem'
HOST = os.environ['HOST']
PORT = 5000
WEBHOOK_HOST = os.environ['HOST']
WEBHOOK_PORT = 443
WEBHOOK_URL_BASE = 'https://{!s}:{}'.format(WEBHOOK_HOST, WEBHOOK_PORT)
#TOKEN = '246271863:AAEUJQJ7aHByov0wnHBjSUGseL1ixU1mSgk'
TOKEN = os.environ['TG_TOKEN']
VK_TOKEN = os.environ['VK_TOKEN']
DEBUG = True
TESTING = True
CELERY_BROKER_URL  = 'redis://localhost:6379/0'
#DATABASE = 'bot.db'
GROUPS = (
    {
        'name':'«Незабываемая Москва» - экскурсии по Москве',
        'url':'unforgettable.moscow',
    },
    {
      'name':'',
      'url':'mospeshkom'
    },
     {
      'name':'',
      'url':'msk_stepbystep'
    },
    {
      'name':'',
      'url':'neobichnie_ekskursii_po_moskve'
    },
    {
      'name':'',
      'url':'pomoscowe'
    },
    {
      'url':'bonmos',
       'name':''
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
