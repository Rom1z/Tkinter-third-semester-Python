import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calculate_triangle():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
            messagebox.showerror("Ошибка", "Треугольник не существует или не удовлетворяет ограничениям.")
        else:
            if a == b == c:
                result_label.config(text="Это равносторонний треугольник.")
            elif a == b or a == c or b == c:
                result_label.config(text="Это равнобедренный треугольник.")
            else:
                result_label.config(text="Это разносторонний треугольник.")

            s = (a + b + c) / 2
            area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
            result_label.config(text=f"Площадь треугольника: {area:.2f}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа для длин сторон треугольника.")

# Создание главного окна
root = tk.Tk()
root.title("Определение треугольника")

# Создание и размещение виджетов
label_a = ttk.Label(root, text="Длина стороны a:")
label_a.grid(row=0, column=0, padx=10, pady=5, sticky="E")
entry_a = ttk.Entry(root)
entry_a.grid(row=0, column=1, padx=10, pady=5)

label_b = ttk.Label(root, text="Длина стороны b:")
label_b.grid(row=1, column=0, padx=10, pady=5, sticky="E")
entry_b = ttk.Entry(root)
entry_b.grid(row=1, column=1, padx=10, pady=5)

label_c = ttk.Label(root, text="Длина стороны c:")
label_c.grid(row=2, column=0, padx=10, pady=5, sticky="E")
entry_c = ttk.Entry(root)
entry_c.grid(row=2, column=1, padx=10, pady=5)

calculate_button = ttk.Button(root, text="Рассчитать", command=calculate_triangle)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = ttk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, pady=5)

# Запуск главного цикла приложения
root.mainloop()