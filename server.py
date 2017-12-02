#-*- coding:utf-8 -*-
import logging
from flask import Flask
import telebot
import config

app = Flask(__name__)
app.debug = config.DEBUG

bot = telebot.TeleBot(config.TOKEN)
telebot.logger.setLevel(logging.DEBUG)

from view import *

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


if __name__ == '__main__':
   if  getattr(config,'TESTING'):
       print('Run testing version.')
       bot.polling()

   else:
       print('Develop version.')
       app.run(
           host = '127.0.0.1',
           port = 5000,
       )
