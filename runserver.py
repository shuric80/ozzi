#! env/bin/python3
#-*- coding:utf-8 -*-

from flask import Flask

from app.log import logger
from app import config

app = Flask(__name__)

from app import views
from app import botviews
from app.top import bot


if __name__ == '__main__':
    logger.info('Run server')

    if getattr(config,"TESTING"):
        bot.polling(none_stop = True)

    else:
       app.run(
          host = config.HOST,
          port = config.PORT,
          debug = config.DEBUG
         )
