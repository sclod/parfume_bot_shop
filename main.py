from telebot import types
from db.db import *
from admin import *
from bot_shared import bot
import random



@bot.message_handler(commands=['start'])
def start(message):
    try:
        db = Databases("database.db")
        db.connect()
        if not db.user_exists(message.from_user.id): # Получаем ответ есть ли пользователь в базе
            db.add_user_to_db(message.from_user.id, message.from_user.username, 'user') # Если пользователя нет в базе, добавляем его
            username = db.fetch_name_user(message.from_user.id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("🔰 Головне Меню")
            keyboard.add(button1)
            bot.send_message(message.from_user.id, text=f'<i>🇺🇦 Вітаю {username}, це магазин парфумів. Ви можете здійснювати замовлення найкращих парфюмів! 🇺🇦</i>', reply_markup=keyboard)
        else:
            menu_buttons = types.InlineKeyboardMarkup(row_width=2)
            menu_button = types.InlineKeyboardButton(text='⭐️ Популярне', callback_data='popular')
            menu_button1 = types.InlineKeyboardButton(text='👦🏻 Чоловічі', callback_data='man_parfum')
            menu_button2 = types.InlineKeyboardButton(text='👩🏼 Жіночі', callback_data='woman_parfum')
            menu_button3 = types.InlineKeyboardButton(text='🛍 Зв\'язатись з продавцем', callback_data='help')
            menu_buttons.add(menu_button2, menu_button1, menu_button, menu_button3)
            bot.send_message(message.chat.id, text='Якщо ви не знайшли те, що хотіли - напишіть мені в телеграмм. ⏳ Працюємо з 9:00 до 23:00. Гарного настрою!💫', reply_markup=menu_buttons)

            db.close()
    except Exception as e:
        print(e)
        bot.answer_callback_query(message.from_user.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

# Возврат в стартовое меню
@bot.message_handler(func=lambda message: message.text == "🔰 Головне Меню")
def main_menu(message):
    start(message)

@bot.message_handler(func=lambda message: message.text == "admin-menu")
def main_menu(message):
    admin(message)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        # Сплитим название калбек даты кнопки
        req = call.data.split('_')
        db = Databases("database.db")
        db.connect()
        
        if call.data == 'man_parfum' or 'woman_parfum':
            random_smile = ["🌱","🌿","🍀","🌷","🌹","💐","🍃","🪸","🪻","🪷","🌺","🌸","🌼", "🌊", "🧊"]
            if req[0] == 'man':
                categories = db.fetch_all_categories_for_man()              # Достаём из базы все бренды мужских духов
                main_buttons = types.InlineKeyboardMarkup(row_width=2)
                for category in categories:                 # Перебираем все категории и выводим в кнопку
                    category_name = category['name'] + f" {random.choice(random_smile)}"
                    callback_data = f"category_{category['id']}_man"
                    button = types.InlineKeyboardButton(text=category_name, callback_data=callback_data)
                    main_buttons.add(button)
                main_button = types.InlineKeyboardButton(text='💎 Весь асортимент 💎', callback_data='all_product_man')
                main_button1 = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
                main_buttons.add(main_button, main_button1)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Наявність/На замовлення 🪄', reply_markup=main_buttons)

            if req[0] == 'woman':
                categories = db.fetch_all_categories_for_woman()
                main_buttons = types.InlineKeyboardMarkup(row_width=2)
                for category in categories:
                    category_name = category['name'] + f" {random.choice(random_smile)}"
                    callback_data = f"category_{category['id']}_woman"
                    button = types.InlineKeyboardButton(text=category_name, callback_data=callback_data)
                    main_buttons.add(button)
                main_button = types.InlineKeyboardButton(text='💎 Весь асортимент 💎', callback_data='all_product_woman')
                main_button1 = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
                main_buttons.add(main_button, main_button1)
            
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Наявність/На замовлення 🪄', reply_markup=main_buttons)
    except Exception as e:
        print(e)
        bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Выбираем духи по бренду
    if req[0] == 'category':
        try:
            id_category = req[1]
            numb = 0

            if req[2] == 'man':
                man_products = db.get_man_products_by_category(id_category) # Берём все духи по id категории 
                count_man = db.get_all_count_man_category(id_category) # Берём общее количество духов
                if man_products:
                    product = man_products[numb]
                    id, name, price, descr, image_url = product

                    markup_order = types.InlineKeyboardMarkup(row_width=1)
                    button1 = types.InlineKeyboardButton(text='🔚', callback_data=f'cat_{id_category}_m_{numb-1}')
                    button2 = types.InlineKeyboardButton(text=f'{numb+1} / {count_man}', callback_data='b')
                    button3 = types.InlineKeyboardButton(text='🔜', callback_data=f'cat1_{id_category}_m_{numb+1}')
                    markup_order.row(button1, button2, button3)
                    button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                    button5 = types.InlineKeyboardButton(text='Назад 🔙', callback_data='man')
                    markup_order.row(button4)
                    markup_order.row(button5)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'<a href="{image_url}">&#8205;</a>', reply_markup=markup_order)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')

            if req[2] == 'woman':
                woman_products = db.get_woman_products_by_category(id_category)     # Достаём товар по выбранной категории
                count_woman = db.get_all_count_woman_category(id_category)    # Достаём общее количество товар определённой категории 
                if woman_products:
                    product = woman_products[numb]
                    id, name, price, descr, image_url = product

                    markup_order = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(text='🔚', callback_data=f'cat_{id_category}_w_{numb-1}')
                    button2 = types.InlineKeyboardButton(text=f'{numb+1} / {count_woman}', callback_data='b')
                    button3 = types.InlineKeyboardButton(text='🔜', callback_data=f'cat1_{id_category}_w_{numb+1}')
                    markup_order.row(button1, button2, button3)
                    button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                    button5 = types.InlineKeyboardButton(text='Назад 🔙', callback_data='woman')
                    markup_order.row(button4)
                    markup_order.row(button5)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'<a href="{image_url}">&#8205;</a>', reply_markup=markup_order)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Листаем товар на -1
    if req[0] == 'cat':
        try:
            id_category = req[1]
            numb = int(req[3])
            if req[2] == 'm':
                products = db.get_man_products_by_category(id_category)
                count_product = db.get_all_count_man_category(id_category)
            if req[2] == 'w':
                products = db.get_woman_products_by_category(id_category)
                count_product = db.get_all_count_woman_category(id_category)
            if numb >= count_product or numb < 0:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
            else:
                if products:
                    product = products[numb]
                    id, name, price, descr, image_url = product

                    markup_order = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(text='🔚', callback_data=f'cat_{id_category}_{req[2]}_{numb-1}')
                    button2 = types.InlineKeyboardButton(text=f'{numb+1} / {count_product}', callback_data='b')
                    button3 = types.InlineKeyboardButton(text='🔜', callback_data=f'cat1_{id_category}_{req[2]}_{numb+1}')
                    markup_order.row(button1, button2, button3)
                    button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                    button5 = types.InlineKeyboardButton(text='Назад 🔙', callback_data='man')
                    markup_order.row(button4)
                    markup_order.row(button5)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'<a href="{image_url}">&#8205;</a>', reply_markup=markup_order)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Листаем товар на +1
    if req[0] == 'cat1':
        try:
            id_category = req[1]
            numb = int(req[3])
            if req[2] == 'm':
                products = db.get_man_products_by_category(id_category)
                count_product = db.get_all_count_man_category(id_category)
            if req[2] == 'w':
                products = db.get_woman_products_by_category(id_category)
                count_product = db.get_all_count_woman_category(id_category)
            if numb >= count_product or numb < 0:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
            else:
                if products:
                    product = products[numb] 
                    id, name, price, descr, image_url = product

                    markup_order = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(text='🔚', callback_data=f'cat_{id_category}_{req[2]}_{numb-1}')
                    button2 = types.InlineKeyboardButton(text=f'{numb+1} / {count_product}', callback_data='b')
                    button3 = types.InlineKeyboardButton(text='🔜', callback_data=f'cat1_{id_category}_{req[2]}_{numb+1}')
                    markup_order.row(button1, button2, button3)
                    button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                    button5 = types.InlineKeyboardButton(text='Назад 🔙', callback_data='woman')
                    markup_order.row(button4)
                    markup_order.row(button5)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'<a href="{image_url}">&#8205;</a>', reply_markup=markup_order)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Показываем все товары, мужские или женские
    if req[0] == 'all':
        try:
            if req[2] == 'man':
                products = db.fetch_all_man_parfum_by_id(1) # Берём все мужские духи
                count_id = db.get_all_count_man()
                if products:
                    current_product = products[0]
                    id, name, price, descr, image_url = current_product

                    test = types.InlineKeyboardMarkup(row_width=3)
                    next_button = types.InlineKeyboardButton(text='<', callback_data=f'prev_{id-1}_m')
                    count_view = types.InlineKeyboardButton(text=f'{id} / {count_id}', callback_data='count')
                    prev_button = types.InlineKeyboardButton(text='>', callback_data=f'next_{id+1}_m')
                    back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data=f'man')
                    button4 = types.InlineKeyboardButton(text='Написать продавцу 🖊', callback_data=f'sendorder_{name}')
                    test.add(next_button, count_view, prev_button, button4)
                    test.add(back_button)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                        f'👑 {name}\n'
                                        f'💵 {price}₴\n'
                                        f'🍀 {descr}\n'
                                        f'<a href="{image_url}">&#8205;</a>'
                                        ,reply_markup=test)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')    
            elif req[2] == 'woman': 
                products = db.fetch_all_woman_pafrum(1)
                count_id = db.get_all_count_woman()
                if products:
                    current_product = products[0]
                    id, name, price, descr, image_url = current_product

                    test = types.InlineKeyboardMarkup(row_width=3)
                    next_button = types.InlineKeyboardButton(text='<', callback_data=f'prev_{id-1}_w')
                    count_view = types.InlineKeyboardButton(text=f'{id} / {count_id}', callback_data='count')
                    prev_button = types.InlineKeyboardButton(text='>', callback_data=f'next_{id+1}_w')
                    back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data=f'woman')
                    button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                    test.add(next_button, count_view, prev_button, button4)
                    test.add(back_button)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                        f'👑 {name}\n'
                                        f'💵 {price}₴\n' 
                                        f'🍀 {descr}\n'
                                        f'<a href="{image_url}">&#8205;</a>'
                                        ,reply_markup=test)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    if req[0] == 'prev':
        try:
            next_id = req[1]
            if req[2] == 'm':
                popular_product = db.fetch_all_man_parfum_by_id(next_id)
                count_id = db.get_all_count_man()
                sex = 'm'
            if req[2] == 'w':
                popular_product = db.fetch_all_woman_pafrum(next_id)
                count_id = db.get_all_count_woman()
                sex = 'w'
            if popular_product:
                current_product = popular_product[0]
                id, name, price, descr, image_url = current_product

                test = types.InlineKeyboardMarkup(row_width=3)
                next_button = types.InlineKeyboardButton(text='<', callback_data=f'prev_{id-1}_{sex}')
                count_view = types.InlineKeyboardButton(text=f'{id} / {count_id}', callback_data='count')
                prev_button = types.InlineKeyboardButton(text='>', callback_data=f'next_{id+1}_{sex}')
                back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
                button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                test.add(next_button, count_view, prev_button, back_button)
                test.add(button4)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'<a href="{image_url}">&#8205;</a>',
                                    reply_markup=test)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')
    
    if req[0] == 'next':
        try:
            next_id = req[1]
            if req[2] == 'm':
                popular_product = db.fetch_all_man_parfum_by_id(next_id)
                count_id = db.get_all_count_man()
                sex = 'm'
            if req[2] == 'w':
                popular_product = db.fetch_all_woman_pafrum(next_id)
                count_id = db.get_all_count_woman()
                sex = 'w'
            if popular_product:
                current_product = popular_product[0]
                id, name, price, descr, image_url = current_product

                test = types.InlineKeyboardMarkup(row_width=3)
                next_button = types.InlineKeyboardButton(text='<', callback_data=f'prev_{id-1}_{sex}')
                count_view = types.InlineKeyboardButton(text=f'{id} / {count_id}', callback_data='count')
                prev_button = types.InlineKeyboardButton(text='>', callback_data=f'next_{id+1}_{sex}')
                back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
                button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                test.add(next_button, count_view, prev_button, button4)
                test.add(back_button)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'<a href="{image_url}">&#8205;</a>',
                                    reply_markup=test)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Меню популярных духов
    if call.data == 'popular':
        try:
            popular_product = db.fetch_all_popular_product(1) # Берём все популярные духи 
            count_id = db.get_all_count_popular()
            if popular_product:
                current_product = popular_product[0]
                id, name, price, descr, image_url, sex = current_product

                test = types.InlineKeyboardMarkup(row_width=3)
                next_button = types.InlineKeyboardButton(text='<', callback_data=f'pop_{id-1}')
                count_view = types.InlineKeyboardButton(text=f'{id} / {count_id}', callback_data='count')
                prev_button = types.InlineKeyboardButton(text='>', callback_data=f'pop1_{id+1}')
                back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
                button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                test.add(next_button, count_view, prev_button, button4)
                test.add(back_button)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'👤 {sex}\n'
                                    f'<a href="{image_url}">&#8205;</a>',
                                    reply_markup=test)
            else: 
                bot.edit_message_text(call.message.chat.id, message_id=call.message.message_id, text="В данной категории нет товаров.")
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Листаем товар на -1
    if req[0] == 'pop':
        try:
            next_id = req[1]
            popular_product = db.fetch_all_popular_product(next_id)
            count_id = db.get_all_count_popular()
            if popular_product:
                current_product = popular_product[0]
                id, name, price, descr, image_url, sex = current_product

                test = types.InlineKeyboardMarkup(row_width=3)
                next_button = types.InlineKeyboardButton(text='<', callback_data=f'pop_{id-1}')
                count_view = types.InlineKeyboardButton(text=f'{id} / {count_id}', callback_data='count')
                prev_button = types.InlineKeyboardButton(text='>', callback_data=f'pop1_{id+1}')
                back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
                button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                test.add(next_button, count_view, prev_button, back_button)
                test.add(button4)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'👤 {sex}\n'
                                    f'<a href="{image_url}">&#8205;</a>',
                                    reply_markup=test)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Листаем товар на +1
    if req[0] == 'pop1':
        try:
            next_id = req[1]
            popular_product = db.fetch_all_popular_product(next_id)
            count_id = db.get_all_count_popular()
            if popular_product:
                current_product = popular_product[0]
                id, name, price, descr, image_url, sex = current_product

                test = types.InlineKeyboardMarkup(row_width=3)
                next_button = types.InlineKeyboardButton(text='<', callback_data=f'pop_{id-1}')
                count_view = types.InlineKeyboardButton(text=f'{id} / {count_id}', callback_data='count')
                prev_button = types.InlineKeyboardButton(text='>', callback_data=f'pop1_{id+1}')
                back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
                button4 = types.InlineKeyboardButton(text='Написати продавцю 🖊', callback_data=f'sendorder_{name}')
                test.add(next_button, count_view, prev_button, back_button)
                test.add(button4)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                                    f'👑 {name}\n'
                                    f'💵 {price}₴\n' 
                                    f'🍀 {descr}\n'
                                    f'👤 {sex}\n'
                                    f'<a href="{image_url}">&#8205;</a>',
                                    reply_markup=test)
            else:
                bot.answer_callback_query(callback_query_id=call.id, text='Більше товарів немає 👻')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')


    if req[0] == 'sendorder':
        try:
            username = db.fetch_name_user(call.from_user.id)
            name_product = req[1]
            if username[0] is None:
                bot.send_message(call.message.chat.id, text='❗️ В вас немає логіна вашого аккаунта телеграмм, напишіть будь-ласка ваш номер телефона в такому форматі - 🇺🇦0999999999, щоб ми з вами зв\'язалися або напишіть мені ❗️')
                bot.register_next_step_handler(call.message, procces_number_client, name_product)
            else:
                bot.send_message(call.message.chat.id, text='Замовлення готово, с вами зв\'яжется продавець 💌')
                bot.send_message(318952676, text=f'🛍 Клієнт @{username} зробив замовлення 🛍\n{name_product}')
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Связь с продавцом
    if call.data == 'help':
        help_buttons = types.InlineKeyboardMarkup(row_width=1)
        help_button1 = types.InlineKeyboardButton(text='🔗Зв\'язатись з продавцем🔗', url='https://t.me/excusemuar')
        help_button2 = types.InlineKeyboardButton(text='🔗Посилання на інстаграм🔗', url='https://www.instagram.com/parfumer.uaa/')
        help_button3 = types.InlineKeyboardButton(text='Назад 🔙', callback_data='main-menu')
        help_buttons.add(help_button1, help_button2, help_button3)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text='♿️Підтримка♿️', reply_markup=help_buttons)

    
    if call.data == 'edit-product-menu':
        edit_buttons = types.InlineKeyboardMarkup(row_width=1)
        buttonedit = types.InlineKeyboardButton(text='Популярне', callback_data=f'edit-req_popular')
        button1edit = types.InlineKeyboardButton(text='Жіночі парфуми', callback_data=f'edit-req_womanparfum')
        button2edit = types.InlineKeyboardButton(text='Чоловічі парфуми', callback_data=f'edit-req_manparfum')
        button3edit = types.InlineKeyboardButton(text='Женские бренды', callback_data='edit-req_womancategory')
        button4edit = types.InlineKeyboardButton(text='Мужские бренды', callback_data='edit-req_mancategory')
        back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data='admin-menu')
        edit_buttons.add(buttonedit, button1edit, button2edit, button3edit, button4edit, back_button)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text='♿️Выбирите какой товар хотите редактировать♿️', reply_markup=edit_buttons)

    ''' Функции для работы c редоктированием товара в бд '''
    # ------------------------------------------------------------------------------------------------------
    # Редактировать Товар
    if req[0] == "edit-req":
        name_table = req[1]
        count_id = db.fetch_count_products_in_table(name_table)
        popular_product = db.fetch_name_products_in_table(name_table)
        admin_edit_buttons = types.InlineKeyboardMarkup()
        for product_tuple in popular_product:
            product_name = product_tuple[0]
            admin_edit_button = types.InlineKeyboardButton(text=f'{product_name}', callback_data=f'rename_{product_name}_{name_table}')
            delete_button = types.InlineKeyboardButton(text='❌', callback_data=f'delete-product_{product_name}_{name_table}')
            admin_edit_buttons.add(admin_edit_button, delete_button)
        back_button = types.InlineKeyboardButton(text='Назад 🔙', callback_data='admin-menu')
        admin_edit_buttons.add(back_button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text='♿️Все продукты данной категории♿️ ',  reply_markup=admin_edit_buttons)

    # Выбор что хотите изменить
    if req[0] == 'rename':
        name_product = req[1]
        name_table = req[2]
        remove_buttons = types.InlineKeyboardMarkup()
        remove_button = types.InlineKeyboardButton(text='Название', callback_data=f'name_{name_product}_{name_table}')
        remove_button1 = types.InlineKeyboardButton(text='Цену', callback_data=f'price_{name_product}_{name_table}')
        remove_button2 = types.InlineKeyboardButton(text='Описанние', callback_data=f'descr_{name_product}_{name_table}')
        remove_button3 = types.InlineKeyboardButton(text='Ссылка на фото', callback_data=f'imageurl_{name_product}_{name_table}')
        remove_button4 = types.InlineKeyboardButton(text='Номер категории', callback_data=f'categoryid_{name_product}_{name_table}')
        remove_buttons.add(remove_button, remove_button1, remove_button2, remove_button3, remove_button4)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text='♿️Что хотите изменить♿️ ',  reply_markup=remove_buttons)
    
    # Изменяем товар
    if req[0] == 'name' or req[0] == 'price' or req[0] == 'descr' or req[0] == 'imageurl' or req[0] == 'categoryid':
        name_column = req[0]
        name_product = req[1]
        name_table = req[2]
        bot.send_message(call.message.chat.id, text='Напишите изменение:')
        bot.register_next_step_handler(call.message, procces_edit_product1, name_table, name_column, name_product)

    # Удаление товара с бд
    if req[0].startswith('delete-product'):
        name_product = req[1]
        name_table = req[2]
        db.delete_product(name_product, name_table)
        bot.answer_callback_query(callback_query_id=call.id, text='Удалено')



    # Запрос на ввод имени бренда которого вы хотите добавить
    if req[0] == 'add-brand':
        try:
            category_name = req[1]
            print(category_name)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Напишите Бренд которую хотите добавить:', )
            bot.register_next_step_handler(call.message, procces_brand_name, category_name)
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Добавляем мужские
    if call.data == 'add_man_parfum':
        try:
            category = req[1]
            name_table = req[1] + req[2]
            results = db.fetch_all_man_category_and_id()
            formatted_text = "\n".join([f"{item[0]} - {item[1]}" for item in results])
            bot.send_message(call.message.chat.id, text=formatted_text)
            bot.send_message(call.message.chat.id, text='Название продукта:')
            bot.register_next_step_handler(call.message, proces_add_product_in_table_part1, name_table)
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')
    
    # Добавляем женские
    if call.data == 'add_woman_parfum':
        try:
            category = req[1]
            name_table = req[1] + req[2]
            results = db.fetch_all_woman_category_and_id()
            formatted_text = "\n".join([f"{item[0]} - {item[1]}" for item in results])
            bot.send_message(call.message.chat.id, text=formatted_text)
            bot.send_message(call.message.chat.id, text='Название продукта:')
            bot.register_next_step_handler(call.message, proces_add_product_in_table_part1, name_table)
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')


    # Добавляем духи в популярное
    if call.data == 'add-popular':
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Название:', )
            bot.register_next_step_handler(call.message, procces_popular_name_part1)
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Возвращаемся в главное меню админа
    if call.data == 'admin-menu':
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            admin(call.message)
        except Exception as e: 
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

    # Возвращаемся в главное меню
    if call.data == 'main-menu':
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            start(call.message)
        except Exception as e:
            print(e)
            bot.answer_callback_query(callback_query_id=call.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')
    db.close()

# ----------------------------------------------------------------
# Функции обработки сообщений для админа
def procces_popular_name_part1(message):
    db = Databases("database.db")
    db.connect()
    try:
        name_product = message.text
        result = db.check_unical(name_product)
        if result == 'Такой товар существует':
            msg = bot.send_message(message.chat.id, result)
        else:
            msg_name = name_product  # Сохраняем имя продукта
            msg = bot.send_message(message.from_user.id, text='Введите цену продукта:')
            bot.register_next_step_handler(msg, procces_popular_name_part2, name_product, msg_name)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')
    db.close()

def procces_popular_name_part2(message, name_product, msg_name):
    try:
        msg_price = message.text
        msg_discr = bot.send_message(message.from_user.id, "Скинь ссылку картинки с инсты, ток глянь появляется ли картинка в телеге, если она не появится, то она не будет отображаться в боте")
        bot.register_next_step_handler(msg_discr, procces_popular_name_part3, name_product, msg_name, msg_price)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

def procces_popular_name_part3(message, name_product, msg_name, msg_price):
    try:
        image_path = message.text
        msg_sex = bot.send_message(message.from_user.id, "Мужской, женский, унисекс?")
        bot.register_next_step_handler(msg_sex, procces_popular_name_part4, name_product, msg_name, msg_price, image_path)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

def procces_popular_name_part4(message, name_product, msg_name, msg_price, image_path):
    try:
        msg_sex = message.text
        product_description = bot.send_message(message.from_user.id, "Введите описание товара:")
        bot.register_next_step_handler(product_description, procces_popular_name_part5, name_product, msg_name, msg_price, image_path, msg_sex)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

def procces_popular_name_part5(message, name_product, msg_name, msg_price, image_path, msg_sex):
    try:
        product_description = message.text
        db = Databases("database.db")
        db.connect()
        
        db.insert_product_in_popular(name_product, msg_price, product_description, image_path, msg_sex)
        bot.send_message(message.from_user.id, "Товар успешно добавлен в таблицу 'popular'")
        admin(message)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')
    db.close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Функции для обработки добавления товара в таблицу 'manparfume
def proces_add_product_in_table_part1(message, name_table):
    try:
        name_table_test = name_table
        name_product = message.text
        print(name_table_test)
        bot.send_message(message.chat.id, text='Введите цену продукта:')
        bot.register_next_step_handler(message, proces_add_product_in_table_part2, name_product, name_table_test)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Щось пішло не так, спробуйте ще раз👁‍🗨')

def proces_add_product_in_table_part2(message, name_product, name_table_test):
    try:
        price = float(message.text)
        bot.send_message(message.chat.id, text='Введите описание товара:')
        bot.register_next_step_handler(message, proces_add_product_in_table_part3, name_product, price, name_table_test)
    except ValueError:
        bot.send_message(message.chat.id, text='Пожалуйста, введите корректную цену:')

def proces_add_product_in_table_part3(message, name_product, price, name_table_test):
    try:
        description = message.text
        bot.send_message(message.chat.id, text='Скиньте ссылку на картинку:')
        bot.register_next_step_handler(message, proces_add_product_in_table_part4, name_product, price, description, name_table_test)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Что-то пошло не так, попробуйте ещё раз👁‍')

def proces_add_product_in_table_part4(message, name_product, price, description, name_table_test):
    try:
        image_url = message.text
        bot.send_message(message.chat.id, text='Введите ID категории:')
        bot.register_next_step_handler(message, proces_add_product_in_table_part5, name_product, price, description, image_url, name_table_test)
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, text='Что-то пошло не так, попробуйте ещё раз👁‍🗨')

def proces_add_product_in_table_part5(message, name_product, price, description, image_url, name_table_test):
    try:
        db = Databases("database.db")
        db.connect()
        print(name_table_test)
        categoryid = int(message.text)
        db.add_product_admin(name_product, price, description, image_url, categoryid, name_table_test)
        bot.send_message(message.chat.id, text='Товар Добавлен!')
    except ValueError:
        bot.send_message(message.chat.id, text='Пожалуйста, введите корректный ID категории.')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, text='Что-то пошло не так, попробуйте ещё раз👁‍🗨')
    db.close()
    admin(message)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Функции для обработки добавления бренда в таблицу        ######## ТУТ ПРОВЕРЬ ДОДИК, Я ИЗМЕНИЛ ПРОВЕРКУ СООБЩЕНИЯ, ЕСЛИ ТЫ НАЖАЛ НА ДОБАВИТЬ БРЕНД И НЕК ДОБОВЛЯЕШЬ ЕГО!!
def procces_brand_name(message, category):
    db = Databases("database.db")
    db.connect()
    name_brand = message.text
    if name_brand == '🔰 Головне Меню':
        admin(message)
    else:
        result = db.insert_name_in_category(name_brand, name_table=category)
        if result == 'Бренд добавлен':
            bot.send_message(message.chat.id, "Бренд успешно добавлен!")
        else:
            bot.send_message(message.chat.id, "Такой бренд уже существует. Введите другое название бренда.")
    db.close()
    admin(message)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Функции для обработки номера телефона клиента
def procces_number_client(message, name_product):
    try:
        number = message.text
        bot.send_message(message.chat.id, text='Замовлення готово, з вами зв\'яжется продавець 💌')
        bot.send_message(318952676, text=f'🛍 Клієнт +38{number} зробив замовлення 🛍\n{name_product}')
    except:
        bot.send_message(message.chat.id, text='Что-то пошло не так, попробуйте ещё раз👁‍🗨')


# На самом то деле этот код полное дерьмо, я его даже переделывать не буду! Но, это мой первый хуебот
def procces_edit_product1(message, name_table, name_column, name_product):
    db = Databases("database.db")
    db.connect()
    try:
        new_value = message.text
        db.edit_product_in_table(name_table, name_column, new_value ,name_product)
        bot.answer_callback_query(callback_query_id=message.id, text='Успешно изменён')
    except Exception as e:
        print(e)
    db.close()
    admin(message)
