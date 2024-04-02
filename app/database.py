import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                description TEXT,
                                manufacturer TEXT,
                                price REAL,
                                quantity INTEGER,
                                photo_path TEXT)''')
        self.connection.commit()

    def execute_query(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id = ?"
        self.cursor.execute(query, (product_id,))
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def add_product(self, name, description, manufacturer, price, quantity, photo_path):
        query = "INSERT INTO products (name, description, manufacturer, price, quantity, photo_path) VALUES (?, ?, ?, ?, ?, ?)"
        values = (name, description, manufacturer, price, quantity, photo_path)
        self.execute_query(query, values)