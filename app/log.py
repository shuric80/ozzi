#-*- coding:utf-8 -*-
import logging
import telebot


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.info('Logger loaded')
