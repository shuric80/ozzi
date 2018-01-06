
#-*- coding:utf-8 -*-
import os.path as ph
import logging
from logging.handlers import RotatingFileHandler
import telebot


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

file_log = ph.join('log','ozzi_bot.log')
handler = RotatingFileHandler(file_log, maxBytes = 100000, backupCount =5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

#logger.addHandler(ch)
logger.addHandler(handler)
logging.debug('Logger loaded')
