#-*- coding:utf-8 -*-

import telebot
from flask import Flask

from app import config

bot = telebot.TeleBot(config.TOKEN)
app = Flask(__name__)
