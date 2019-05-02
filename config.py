# -*- coding:utf-8 -*-
import os
CNT = 10
SESSION_TIME = 3600
SECRET_COD = 'kuku'
WEBHOOK_SSL_CERT = 'certs/webhook_cert.pem'
WEBHOOK_SSL_PRIV = 'certs/webhook_pkey.pem'
HOST = os.environ['HOST']
PORT = 5000
WEBHOOK_HOST = os.environ['HOST']
WEBHOOK_PORT = 8443
WEBHOOK_URL_BASE = 'https://{!s}:{}'.format(WEBHOOK_HOST, WEBHOOK_PORT)
TOKEN = os.environ['TG_TOKEN']
VK_TOKEN = os.environ['VK_TOKEN']
DEBUG = os.environ['DEBUG']
TESTING = False
CELERY_BROKER_URL  = 'redis://localhost:6379/0'
#DATABASE = 'bot.db'
GROUPS = (
    {
        'name':'«Незабываемая Москва» - экскурсии по Москве',
        'url':'unforgettable.moscow',
    },
    {
      'name':'sada',
      'url':'mospeshkom'
    },
     {
      'name':'asd',
      'url':'msk_stepbystep'
    },
    {
      'name':'asdsa',
      'url':'neobichnie_ekskursii_po_moskve'
    },
    {
      'name':'asdsa',
      'url':'pomoscowe'
    },
    {
      'url':'bonmos',
       'name':'adas'
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
