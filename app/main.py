#основной
import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime, timedelta
from fpdf import FPDF

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список товаров")

        self.products = []

        self.tree = ttk.Treeview(root, columns=('Name', 'Description', 'Manufacturer', 'Price'), show='headings')
        self.tree.heading('Name', text='Наименование')
        self.tree.heading('Description', text='Описание')
        self.tree.heading('Manufacturer', text='Производитель')
        self.tree.heading('Price', text='Цена')
        self.tree.pack(expand=True, fill='both')

        self.btn_add = tk.Button(root, text="Добавить", command=self.add_product)
        self.btn_add.pack()

        self.btn_order_info = tk.Button(root, text="Информация о заказе", command=self.order_info)
        self.btn_order_info.pack()

        self.btn_delete = tk.Button(root, text="Удалить", command=self.delete_product)
        self.btn_delete.pack()

        self.pickup_points = ["Пункт выдачи 1", "Пункт выдачи 2", "Пункт выдачи 3"]
        self.pickup_point_combobox = ttk.Combobox(root, values=self.pickup_points, state="readonly")
        self.pickup_point_combobox.pack()


    def add_product(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить товар")

        tk.Label(add_window, text="Наименование:").grid(row=0, column=0, sticky='e')
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Описание:").grid(row=1, column=0, sticky='e')
        description_entry = tk.Entry(add_window)
        description_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Производитель:").grid(row=2, column=0, sticky='e')
        manufacturer_entry = tk.Entry(add_window)
        manufacturer_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Цена:").grid(row=3, column=0, sticky='e')
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=3, column=1)

        add_button = tk.Button(add_window, text="Добавить", command=lambda: self.add_to_treeview(name_entry.get(), description_entry.get(), manufacturer_entry.get(), price_entry.get(), add_window))
        add_button.grid(row=4, columnspan=2)

    def add_to_treeview(self, name, description, manufacturer, price, add_window):
        if name and description and manufacturer and price:
            self.products.append({'Name': name, 'Description': description, 'Manufacturer': manufacturer, 'Price': price})
            self.update_treeview()
            add_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for product in self.products:
            self.tree.insert('', 'end', values=(product['Name'], product['Description'], product['Manufacturer'], product['Price']))

    def delete_product(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = selected_item[0]
            self.tree.delete(item_id)
            self.products.pop(item_id)
        else:
            messagebox.showerror("Ошибка", "Выберите товар для удаления")

    def order_info(self):
        total_price = sum(float(product['Price']) for product in self.products)
        num_products = len(self.products)
        delivery_time = 3 if num_products >= 3 else 6
        code = random.randint(100, 999)
        formatted_code = f"<b>{code}</b>"
        delivery_date = datetime.now() + timedelta(days=delivery_time)
        pickup_point = self.pickup_point_combobox.get()
        messagebox.showinfo("Информация о заказе", f"Количество товаров: {num_products}\nОбщая сумма заказа: {total_price}р\nДата заказа: {datetime.now().strftime('%Y-%m-%d')}\nНомер заказа: {len(self.products)}\nСостав заказа: {', '.join([product['Name'] for product in self.products])}\nСумма заказа: {total_price}р\nПункт выдачи: {pickup_point}\nКод получения: {formatted_code}\nСрок доставки: {delivery_time} дней (до {delivery_date.strftime('%Y-%m-%d')})")

    def buy_product(self):
        selected_item = self.tree.selection ()
        if selected_item:
            item_id = int ( selected_item[0][1:] ) - 1
            if 0 <= item_id < len ( self.products ):
                product = self.products[item_id]
                code = random.randint ( 100 , 999 )
                self.generate_receipt ( product , code )
                messagebox.showinfo ( "Покупка товара" ,
                                      f"Вы купили товар: {product['Name']} по цене {product['Price']}р.\nТалон с кодом отправлен на печать." )
            else:
                messagebox.showerror ( "Ошибка" , "Выберите существующий товар для покупки" )
        else:
            messagebox.showerror ( "Ошибка" , "Выберите товар для покупки" )



if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()