import sqlite3
import logging

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

        # Настройка логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('database.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    # методы enter и exit для менеджера контектса with
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.logger.info("Подключение к базе данных произошло удачно")
        except sqlite3.Error as e:
            self.logger.error(f"Произошла ошибка при подключение к БД: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Подключение к базе данных завершено")

    def execute_query(self, query, params=None):
        self.logger.info(f"Запрос: {query}, параметры: {params}")
        try:
            if params is not None:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Ошибка в запросе к базе данных: {e}")
            return False

    def commit(self):
        if self.conn:
            self.conn.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchall()




# Подключение к бд
with Database('example.db') as db:
    # сюда добавить создание таблиц таблиц
    create_table_query = """
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER
        );
    """
    db.execute_query(create_table_query)

    # как добавлять данные
    insert_query = "INSERT INTO users (name, age) VALUES (?,?);"
    db.execute_query(insert_query, ('Danila Beskrokov', 25))
    db.commit()

    # выборка данных
    select_query = "SELECT * FROM users;"
    db.execute_query(select_query)
    rows = db.fetchall()
    print(rows)