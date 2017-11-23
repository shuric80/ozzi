#-*- coding:utf-8 -*-

#import telebot
from flask import Flask, request, abort

from app import app, bot
from log import logger


@app.route('/bot', methods=['GET', 'HEAD'])
def webhook():
   bot.remove_webhook()
   bot.set_webhook("https://62.109.13.25:8443/bot",  certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
   return '!'


@app.route('/bot', methods=['POST'])
def send_message():
   logger.debug('WEBHOOK: HEADERS:{}  BODY:{}'.format(request.headers, request.data))

   if request.headers.get('content-type') == 'application/json':
       json_string = request.get_data().decode('utf-8')
       update = telebot.types.Update.de_json(json_string)
       bot.process_new_updates([update])
       return ''#

   else:
      logger.error('FAIL HEADERS:{}'.format(request.headers))
