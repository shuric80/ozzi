#-*- coding:utf-8 -*-

import telebot
from flask import  request, abort

from app.top import app, bot
from app.log import logger

from app import config


@app.route('/', methods=['GET', 'HEAD'])
def webhook():
   logger.info('webbhook')
   bot.remove_webhook()
   bot.set_webhook("{}:{}/".format(config.HOST, config.PORT),  certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
   return '!'


@app.route('/', methods=['POST'])
def send_message():
   logger.debug('WEBHOOK: HEADERS:{}  BODY:{}'.format(request.headers, request.data))

   if request.headers.get('content-type') == 'application/json':
       json_string = request.get_data().decode('utf-8')
       update = telebot.types.Update.de_json(json_string)
       bot.process_new_updates([update])
       return ''#

   else:
      logger.error('FAIL HEADERS:{}'.format(request.headers))
