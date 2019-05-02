#-*- coding:utf-8 -*-
import logging
from flask import Flask
from celery import Celery
from datetime import timedelta

import telebot
import config
from log import logger


app = Flask(__name__)
app.debug = config.DEBUG

celery = Celery('ozzi', broker = config.CELERY_BROKER_URL)

bot = telebot.TeleBot(config.TG_TOKEN)


from view import *


@app.route('/ozzi', methods=['GET', 'HEAD'])
def webhook():
    bot.remove_webhook()
    #TODO брать с конфига
    bot.set_webhook(f"{config.HOST}:8443/ozzi",  certificate=open(config.WEBHOOK_SSL_CERT, 'r'))    
    return '!'


@app.route('/ozzi', methods=['POST'])
def send_message():
    logger.info('WEBHOOK: HEADERS:{}  BODY:{}'.format(request.headers, request.data))

    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
        logger.error('FAIL HEADERS:{}'.format(request.headers))


@app.route('/ping')
def index():
    return '<h2>pong</h2>'
