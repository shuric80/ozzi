#-*- coding:utf-8 -*-
import logging
import telebot


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('log/bot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)
logging.debug('Logger loaded')
