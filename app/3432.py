import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, \
    QDialog, QTextEdit, QListWidgetItem
from PyQt5.QtCore import Qt
import mysql.connector
from datetime import datetime, timedelta


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12543hRGB2001",
            database="inventory"
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                             (id INT AUTO_INCREMENT PRIMARY KEY,
                             name VARCHAR(255) NOT NULL,
                             description TEXT,
                             manufacturer VARCHAR(255),
                             price DECIMAL(10, 2),
                             quantity INT)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                             (id INT AUTO_INCREMENT PRIMARY KEY,
                             date DATETIME NOT NULL,
                             status VARCHAR(50) NOT NULL,
                             pickup_point VARCHAR(255),
                             delivery_date DATE)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS order_items
                             (id INT AUTO_INCREMENT PRIMARY KEY,
                             order_id INT,
                             product_id INT,
                             quantity INT,
                             FOREIGN KEY(order_id) REFERENCES orders(id),
                             FOREIGN KEY(product_id) REFERENCES products(id))''')

    def get_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def add_order(self, items, pickup_point):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "New"
        delivery_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d") if all(item[5] >= 3 for item in items) else \
            (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d")

        self.cursor.execute("INSERT INTO orders (date, status, pickup_point, delivery_date) VALUES (%s, %s, %s, %s)",
                            (date, status, pickup_point, delivery_date))
        order_id = self.cursor.lastrowid

        for item in items:
            self.cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                                (order_id, item[0], 1))
        self.connection.commit()
        return order_id

    def update_quantity(self, product_id, quantity):
        self.cursor.execute("UPDATE products SET quantity=%s WHERE id=%s", (quantity, product_id))
        self.connection.commit()


class ProductListWidget(QWidget):
    def __init__(self, parent=None):
        super(ProductListWidget, self).__init__(parent)
        self.db = Database()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.populate_list()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def populate_list(self):
        products = self.db.get_products()
        for product in products:
            item = QListWidgetItem(product[1])
            item.setData(Qt.UserRole, product)
            self.list_widget.addItem(item)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Терминал заказа")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.product_list_widget = ProductListWidget()
        self.main_layout.addWidget(self.product_list_widget)

        self.order_button = QPushButton("Просмотр заказа")
        self.order_button.setEnabled(False)
        self.order_button.clicked.connect(self.show_order)
        self.main_layout.addWidget(self.order_button)

    def show_order(self):
        dialog = OrderDialog(self)
        dialog.exec_()


class OrderDialog(QDialog):
    def __init__(self, parent=None):
        super(OrderDialog, self).__init__(parent)
        self.setWindowTitle("Просмотр заказа")
        self.db = Database()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Fetching order details
        # For simplicity, assume there's only one order and fetch it
        order_id = 1
        self.order = self.fetch_order(order_id)

        # Display order details
        order_info_label = QLabel(f"Номер заказа: {self.order[0]}")
        layout.addWidget(order_info_label)

        items_label = QLabel("Состав заказа:")
        layout.addWidget(items_label)

        items_text_edit = QTextEdit()
        items_text_edit.setReadOnly(True)
        items_text_edit.setPlainText(self.order_items_to_string())
        layout.addWidget(items_text_edit)

        total_price_label = QLabel(f"Сумма заказа: {self.calculate_total_price()} руб.")
        layout.addWidget(total_price_label)

        pickup_point_label = QLabel(f"Пункт выдачи: {self.order[3]}")
        layout.addWidget(pickup_point_label)

        pickup_code_label = QLabel(f"Код получения: <b>{self.generate_pickup_code()}</b>")
        layout.addWidget(pickup_code_label)

        self.setLayout(layout)

    def fetch_order(self, order_id):
        self.db.cursor.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
        return self.db.cursor.fetchone()

    def fetch_order_items(self, order_id):
        self.db.cursor.execute("SELECT products.name, products.price FROM order_items JOIN products ON "
                               "order_items.product_id=products.id WHERE order_items.order_id=%s", (order_id,))
        return self.db.cursor.fetchall()

    def order_items_to_string(self):
        items = self.fetch_order_items(self.order[0])
        items_string = ""
        for item in items:
            items_string += f"{item[0]} - {item[1]} руб.\n"
        return items_string

    def calculate_total_price(self):
        items = self.fetch_order_items(self.order[0])
        return sum(item[1] for item in items)

    def generate_pickup_code(self):
        return ''.join(random.choices('0123456789', k=3))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())