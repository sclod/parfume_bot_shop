import telebot
from db.db import *

bot = telebot.TeleBot("6605423977:AAEf0qtN7FWfhCLirsxu_nEEnBVjqTjIJYM",parse_mode='HTML')

db = Databases("database.db")
db.connect()
db.create_table_users()
db.create_table_man()
db.create_table_woman()
db.create_table_popular()
db.create_table_category()
