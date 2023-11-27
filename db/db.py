import sqlite3

class Databases():
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = sqlite3.connect(self.db_name)
        self.cursor = self.db.cursor()

    # Таблица пользователей
    def create_table_users(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                status TEXT
            )
        ''')
        self.db.commit()

    # Таблица Мужских парфюмов
    def create_table_man(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS manparfum (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                imageurl TEXT,
                categoryid INTEGER,
                FOREIGN KEY (categoryid) REFERENCES man_category(id)
            )
        ''')
        self.db.commit()
    
    # Таблица Женских духов
    def create_table_woman(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS womanparfum (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                imageurl TEXT,
                categoryid INTEGER,
                FOREIGN KEY (categoryid) REFERENCES womancategory(id)
            )
        ''')
        self.db.commit()

    # Таблица Популярных духов
    def create_table_popular(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS popular (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INT,
                descr TEXT,
                imageurl TEXT,
                sex TEXT
            )
        ''')
        self.db.commit()

    # Таблица Мужских брендов
    def create_table_category(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mancategory (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS womancategory (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        self.db.commit()

    ''' Функции для работы с таблицой users '''
    # ------------------------------------------------------------------------------------------------------
    # Проверка пользователя
    def get_user_status(self, user_id):
        self.cursor.execute('SELECT status FROM users WHERE id = ?', (user_id, ))
        status = self.cursor.fetchone()
        return status[0] if status else None

    # Проверка есть ли пользователь в бд
    def user_exists(self, user_id):
        self.cursor.execute("SELECT id FROM users WHERE id = ?", (user_id, ))
        result = self.cursor.fetchone()
        return result is not None

    # Добавляем пользователя в таблицу users
    def add_user_to_db(self, user_id, user_name, status):
        self.cursor.execute("INSERT INTO users (id, name, status) VALUES (?, ?, ?)", (user_id, user_name, status))
        self.db.commit()

    # Берём логин пользователя
    def fetch_name_user(self, user_id):
        self.cursor.execute('SELECT name FROM users WHERE id = ?', (user_id, ))
        return self.cursor.fetchone()[0]

    # ------------------------------------------------------------------------------------------------------
    ''' Функции для работы с мужской таблицой '''
    # ------------------------------------------------------------------------------------------------------
    # Возвращаем общее количество товаров с таблицы "manparfum" по id категории
    def get_all_count_man_category(self, category_id):
        result = self.cursor.execute('SELECT COUNT(*) FROM manparfum WHERE categoryid = ?', (category_id, )).fetchone()[0]
        return result

    # Возвращаем все товары с id, имя, цена, описание и картинку с таблицы "manparfum" по id категории
    def get_man_products_by_category(self, category_id):
        self.cursor.execute("SELECT id, name, price, descr, imageurl FROM manparfum WHERE categoryid = ?", (category_id, ))
        return self.cursor.fetchall()

    # Возвращаем все товары с id, имя, цена, описание и картинку с таблицы "manparfum"  
    def fetch_all_man_parfum_by_id(self, id):
        self.cursor.execute("SELECT id, name, price, descr, imageurl FROM manparfum WHERE id = ?", (id, ))
        return self.cursor.fetchall()

    # Возвращаем все категории с таблицы "man_category"
    def fetch_all_categories_for_man(self):
        self.cursor.execute("SELECT * FROM mancategory")
        categories = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1]} for row in categories]
    
    # Возвращаем общее количество товаров с таблици "manparfum"
    def get_all_count_man(self):
        result = self.cursor.execute('SELECT COUNT(*) FROM manparfum').fetchone()[0]
        return result

    # ------------------------------------------------------------------------------------------------------
    ''' Функции для работы с женской таблицой '''
    # ------------------------------------------------------------------------------------------------------
    # Возвращаем все товары с id, имя, цена, описание и картинку с таблицы "womanparfum" по id категории
    def get_woman_products_by_category(self, category_id):
        self.cursor.execute("SELECT id, name, price, descr, imageurl FROM womanparfum WHERE categoryid = ?", (category_id, ))
        return self.cursor.fetchall()

    # Возвращаем общее количество товаров с таблицы "womanparfum" по id категории
    def get_all_count_woman_category(self, category_id):
        result = self.cursor.execute('SELECT COUNT(*) FROM womanparfum WHERE categoryid = ?', (category_id, )).fetchone()[0]
        return result

    # Возвращаем все категории с таблицы "woman_category"
    def fetch_all_categories_for_woman(self):
        self.cursor.execute("SELECT * FROM womancategory")
        categories = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1]} for row in categories]

    # Возвращаем все товары с id, имя, цена, описанние и картника с таблицы "womanparfum"
    def fetch_all_woman_pafrum(self, id):
        self.cursor.execute("SELECT id, name, price, descr, imageurl FROM womanparfum Where id = ?", (id, ))
        return self.cursor.fetchall()

    # Возвращаем общее количество товаров с таблици "wonanparfum"
    def get_all_count_woman(self):
        result = self.cursor.execute('SELECT COUNT(*) FROM womanparfum').fetchone()[0]
        return result
    # ------------------------------------------------------------------------------------------------------

    ''' Функции для работы с популярной таблицой '''
    # Возвращаем все товары с id, имя, цена, описанние и картника с таблицы "popular" 
    def fetch_all_popular_product(self, id):
        self.cursor.execute("SELECT id, name, price, descr, imageurl, sex FROM popular Where id = ?", (id, ))
        return self.cursor.fetchall()

    # Возвращаем общее количество товаров с таблици "popular"
    def get_all_count_popular(self):
        result = self.cursor.execute('SELECT COUNT(*) FROM popular').fetchone()[0]
        return result
    # ------------------------------------------------------------------------------------------------------

    # Функции для админа
    # ------------------------------------------------------------------------------------------------------
    # Добавление бренда в бд и проверка на уникальность
    def insert_name_in_category(self, name, name_table):
        print(name_table)
        list = self.cursor.execute(f'SELECT name FROM {name_table} WHERE name = "{name}"').fetchone()
        if list:
            return 'Такой бренд существует'
        else:
            self.cursor.execute(f"INSERT INTO {name_table} (name) VALUES(?)", (name,))
            self.db.commit()
            return 'Бренд добавлен'
    
    # Добавление товара в таблицу 'popular'
    def insert_product_in_popular(self, name, price, descr, image_url, sex):
        self.cursor.execute("INSERT INTO popular (name, price, descr, imageurl, sex) VALUES (?, ?, ?, ?, ?)", (name, price, descr, image_url, sex))
        self.db.commit()

    # Проверка на уникальность имени в таблице 'popular'
    def check_unical(self, name):
        existing_name = self.cursor.execute('SELECT name FROM popular WHERE name = ?', (name,)).fetchone()
        if existing_name:
            return 'Такой товар существует'
        else:
            return 'Введите цену товара:'

    # Берём все мужские категории 
    def fetch_all_man_category_and_id(self):
        result = self.cursor.execute("SELECT id, name FROM mancategory")
        return result.fetchall()

    # Берём все женские категории
    def fetch_all_woman_category_and_id(self):
            result = self.cursor.execute("SELECT id, name FROM womancategory")
            return result.fetchall()

    # Добавление парфюма в переданую таблицу
    def add_product_admin(self, name, price, descr, image_url, categoryid, table_name):
        self.cursor.execute(f"INSERT INTO {table_name} (name, price, descr, imageurl, categoryid) VALUES (?, ?, ?, ?, ?)", (name, price, descr, image_url, categoryid))
        self.db.commit()

    # Все общии фунцкии
    # ------------------------------------------------------------------------------------------------------
    # Возращаем названия товара с таблицы которую передали
    def fetch_name_products_in_table(self, name_table):
        result = self.cursor.execute(f'SELECT name FROM {name_table}')
        return result.fetchall()
    
    # Возвращаем количество товаров с таблицы которую передали
    def fetch_count_products_in_table(self, name_table):
        result = self.cursor.execute(f'SELECT COUNT(*) FROM {name_table}').fetchone()[0]
        return result

    # Изменяем параметры выбраного продукта
    def edit_product_in_table(self, name_table, name_column, new_value, name_product):
        if name_table == 'popular' and name_column == 'categoryid':
            self.cursor.execute(f'UPDATE {name_table} SET sex = ? WHERE name = ?', (new_value, name_product))
        else:
            self.cursor.execute(f'UPDATE {name_table} SET {name_column} = ? WHERE name = ?', (new_value, name_product))
        self.db.commit()
    # ------------------------------------------------------------------------------------------------------
    # Удаление товара с базы
    def delete_product(self, name_product, name_table):
        self.cursor.execute(f"DELETE FROM {name_table} WHERE name = ?", (name_product,))
        self.db.commit()

    # Закрыть подключение к базе 
    def close(self):
        self.cursor.close()
        self.db.close()
    # -------------------------------------------------------------------------------------------------------
