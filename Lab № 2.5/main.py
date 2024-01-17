import tkinter as tk
from tkinter import ttk

def on_calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operator = operator_combobox.get()

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            result = num1 / num2
        else:
            result = "Ошибка: неверный оператор"

        result_label.config(text=f"Результат: {result}")
    except ValueError:
        result_label.config(text="Ошибка ввода. Пожалуйста, введите числовые значения.")

# Создание главного окна
root = tk.Tk()
root.title("Простой калькулятор")

# Создание и размещение элементов интерфейса
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Число 1:").grid(row=0, column=0, sticky=tk.W)
entry_num1 = ttk.Entry(frame)
entry_num1.grid(row=0, column=1)

ttk.Label(frame, text="Оператор:").grid(row=1, column=0, sticky=tk.W)
operators = ["+", "-", "*", "/"]
operator_combobox = ttk.Combobox(frame, values=operators)
operator_combobox.grid(row=1, column=1)

ttk.Label(frame, text="Число 2:").grid(row=2, column=0, sticky=tk.W)
entry_num2 = ttk.Entry(frame)
entry_num2.grid(row=2, column=1)

calculate_button = ttk.Button(frame, text="Вычислить", command=on_calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Запуск главного цикла
root.mainloop()