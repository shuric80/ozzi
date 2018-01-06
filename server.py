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

bot = telebot.TeleBot(config.TOKEN)


from view import *

# @celery.on_after_configure.connect
# def task(sender, **kwargs):
#     sender.add_periodic_task(1, test.s('PING'), name= 'add every 10')

#@celery.task
#def test():
#     logger.debug('PING')


@app.route('/bot', methods=['GET', 'HEAD'])
def webhook():
    bot.remove_webhook()
    bot.set_webhook("https://62.109.13.25:8443/bot",  certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
    return '!'


@app.route('/bot', methods=['POST'])
def send_message():
    logger.info('WEBHOOK: HEADERS:{}  BODY:{}'.format(request.headers, request.data))

    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
        logger.error('FAIL HEADERS:{}'.format(request.headers))
