# -*- coding:utf-8 -*-
<<<<<<< HEAD:app/config.py
PORT = 5000
HOST = "127.0.0.1"
CNT = 20
=======

CNT = 10
SESSION_TIME = 3600
>>>>>>> af55829:config.py
SECRET_COD = 'kuku'
#TOKEN = '246271863:AAEUJQJ7aHByov0wnHBjSUGseL1ixU1mSgk'
TOKEN = '163963654:AAGaVG5vMSfZ5nuGV9q5FyGcojW-ShoJR0k'
VK_TOKEN = '54cbe13354cbe13354cbe1334054975dd8554cb54cbe1330d8ffa0ce43119178d2f7ead'
DEBUG = True
TESTING = True
DATABASE = 'bot.db'
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
    }


)

#TODO add text for help
HELP = """
Бот может многое:
  /last — 5 последних новостей
  /last 1 — Последняя новость. Вообще, можно ввести любую цифру от 1 до 10, бот поймет.
  /list - выдаст полные список групп.
"""
