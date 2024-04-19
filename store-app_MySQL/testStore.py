import tkinter as tk
from tkinter import ttk, Menu, Toplevel, messagebox
import mysql.connector
from PIL import Image, ImageTk
import random
import datetime

# Establishing a connection to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12543hRGB2001",
    database="magazine"
)
mycursor = mydb.cursor()

root = tk.Tk()
root.title("Магазин")
root.geometry("1000x700")
root.configure(background='#f0f0f0')  # Setting background color

order = []
total_price = 0
pickup_points = ["Пункт выдачи 1", "Пункт выдачи 2", "Пункт выдачи 3"]
selected_pickup = tk.StringVar(value=pickup_points[0])

# Function to fetch products from the database
def get_products():
    mycursor.execute("SELECT id, photo, name, description, manufacturer, price FROM products")
    products = mycursor.fetchall()

    for idx, product in enumerate(products):
        img = Image.open(product[1])
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        product_frame = ttk.Frame(root, padding=10, style="Product.TFrame")  # Apply custom style
        product_frame.grid(row=0, column=idx, padx=10)

        label = ttk.Label(product_frame, image=img)
        label.image = img
        label.grid(row=0, column=0)

        ttk.Label(product_frame, text=f"Название: {product[2]}", style="ProductName.TLabel").grid(row=1, column=0)
        ttk.Label(product_frame, text=f"Описание: {product[3]}", style="ProductDesc.TLabel").grid(row=2, column=0)
        ttk.Label(product_frame, text=f"Цена: {product[5]}", style="ProductPrice.TLabel").grid(row=3, column=0)

        context_menu = Menu(root, tearoff=0)
        context_menu.add_command(label="Добавить к заказу", command=lambda prod=product: add_to_order(prod))
        label.bind("<Button-3>", lambda e, context_menu=context_menu: context_menu.post(e.x_root, e.y_root))

# Function to add a product to the order
def add_to_order(product):
    global total_price, order
    order.append(product)
    total_price += product[5]
    update_order_button()

# Function to remove a product from the order
def remove_from_order(product):
    global total_price, order
    order.remove(product)
    total_price -= product[5]
    update_order_window()

# Function to save order details to the database
def save_order_to_db():
    global total_price
    order_date = datetime.datetime.now().strftime("%Y-%m-%d")
    pickup_point = selected_pickup.get()
    status = "Новый"

    sql = "INSERT INTO orders (total_price, pickup_point, status) VALUES (%s, %s, %s)"
    val = (total_price, pickup_point, status)
    mycursor.execute(sql, val)
    mydb.commit()

    order_id = mycursor.lastrowid

    order_number = f"ORD-{order_id}"
    sql_update = "UPDATE orders SET order_number = %s WHERE order_id = %s"
    val_update = (order_number, order_id)
    mycursor.execute(sql_update, val_update)
    mydb.commit()

    messagebox.showinfo("Сохранено", f"Заказ успешно сохранен в базе данных. Номер заказа: {order_number}")

# Function to save order details to a PDF file
def save_order():
    global order
    save_order_to_db()
    order_date = datetime.datetime.now().strftime("%Y-%m-%d")
    order_number = generate_order_code()
    pickup_code = generate_order_code()
    delivery_time = get_delivery_time(len(order))

    pdf_filename = f"order_{order_number}.pdf"
    # Rest of the code remains the same as yours...

# Function to generate a random order code
def generate_order_code():
    return f"{random.randint(100, 999)}"

# Function to calculate delivery time based on the number of items in the order
def get_delivery_time(order_length):
    return "3 дня" if order_length >= 3 else "6 дней"

# Function to display the order in a separate window
def view_order():
    global order_window
    order_window = Toplevel(root)
    order_window.title("Заказы")
    order_window.geometry("700x800")

    update_order_window()

# Function to update the order window with the current order details
def update_order_window():
    global total_price_label, pickup_combobox, save_order_btn

    for widget in order_window.winfo_children():
        widget.destroy()

    for idx, product in enumerate(order):
        img = Image.open(product[1])
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        product_frame = ttk.Frame(order_window, padding=10)
        product_frame.grid(row=idx, column=0)

        label = ttk.Label(product_frame, image=img)
        label.image = img
        label.grid(row=0, column=0)

        ttk.Label(product_frame, text=f"Название: {product[2]}").grid(row=1, column=0)
        ttk.Label(product_frame, text=f"Описание: {product[3]}").grid(row=2, column=0)
        ttk.Label(product_frame, text=f"Цена: {product[5]}").grid(row=3, column=0)

        remove_btn = ttk.Button(product_frame, text="Удалить", command=lambda prod=product: remove_from_order(prod))
        remove_btn.grid(row=4, column=0, pady=5)

    total_price_label = ttk.Label(order_window, text=f"Общая стоимость: {total_price}")
    total_price_label.grid(row=len(order) + 1, column=0, pady=10)

    ttk.Label(order_window, text="Выберите пункт выдачи:").grid(row=len(order) + 2, column=0, pady=5)
    pickup_combobox = ttk.Combobox(order_window, textvariable=selected_pickup, values=pickup_points, state="readonly")
    pickup_combobox.grid(row=len(order) + 3, column=0, pady=5)

    save_order_btn = ttk.Button(order_window, text="Сохранить", command=save_order)
    save_order_btn.grid(row=len(order) + 4, column=0, pady=10)

# Applying custom styles
root.style = ttk.Style()
root.style.theme_use('clam')

root.style.configure("Product.TFrame", background='#ddeeff', borderwidth=2)
root.style.configure("ProductName.TLabel", background='#ddeeff', foreground='#333333', font=('Arial', 10, 'bold'))
root.style.configure("ProductDesc.TLabel", background='#ddeeff', foreground='#333333', font=('Arial', 9))
root.style.configure("ProductPrice.TLabel", background='#ddeeff', foreground='#0080ff', font=('Arial', 9, 'italic'))

# Buttons
root.style.configure("TButton", background='#0080ff', foreground='#ffffff', font=('Arial', 10, 'bold'))
root.style.map("TButton", background=[('active', '#0059b3')])

# Labels
root.style.configure("TLabel", background='#f0f0f0', foreground='#333333', font=('Arial', 10))

# Combobox
root.style.configure("TCombobox", background='#ffffff', foreground='#333333', fieldbackground='#ffffff', font=('Arial', 10))

get_products()

def update_order_button():
    global save_order_btn

    if order:
        view_order_btn.grid(row=len(order) + 2, column=0, pady=10)
        save_order_btn.grid(row=len(order) + 3, column=0, pady=10)
    else:
        view_order_btn.grid_remove()
        save_order_btn.grid_remove()

view_order_btn = ttk.Button(root, text="Просмотр заказа", command=view_order)
view_order_btn.grid(row=1, column=0, pady=10)

save_order_btn = ttk.Button(root, text="Сохранить", command=save_order)
save_order_btn.grid(row=2, column=0, pady=10)

root.mainloop()