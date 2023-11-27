from bot_shared import bot
from db.db import *
from telebot import types

# Основное меню админки
@bot.message_handler(commands=['admin'])
def admin(message):
    db = Databases("database.db")
    db.connect()
    user_status = db.get_user_status(message.from_user.id)
    if user_status == 'admin':
        admin_menu = types.InlineKeyboardMarkup(row_width=1)
        admin_button = types.InlineKeyboardButton(text='Редактировать товар ✍️', callback_data='edit-product-menu')
        admin_button1 = types.InlineKeyboardButton(text='Добавить мужской бренд 👨🏻', callback_data='add-brand_mancategory')
        admin_button2 = types.InlineKeyboardButton(text='Добавить женский бренд 👩🏼', callback_data='add-brand_womancategory')
        admin_button3 = types.InlineKeyboardButton(text='Добавить товар в популярное 🔥', callback_data='add-popular')
        admin_button4 = types.InlineKeyboardButton(text='Добавить мужской парфюм 👃🏻', callback_data='add_man_parfum')
        admin_button5 = types.InlineKeyboardButton(text='Добавить женский парфюм 👃🏻', callback_data='add_woman_parfum')
        admin_menu.add(admin_button, admin_button1, admin_button2, admin_button3, admin_button4, admin_button5)
        bot.send_message(message.chat.id, "<b>💼 Панель администратора</b>"
                                          , parse_mode='HTML', reply_markup=admin_menu)
    else:
      bot.send_message(message.chat.id, text='Вы не админ!')
    
    db.close()
