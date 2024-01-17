import tkinter as tk
from tkinter import ttk
import math


def check_triangle_sides(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return False
    if a + b <= c or a + c <= b or b + c <= a:
        return False
    return True


def determine_triangle_type(a, b, c):
    if not check_triangle_sides(a, b, c):
        return "Невозможный треугольник"

    sides = [a, b, c]
    sides.sort()

    if sides[0] ** 2 + sides[1] ** 2 == sides[2] ** 2:
        return "Прямоугольный треугольник"
    elif sides[0] ** 2 + sides[1] ** 2 < sides[2] ** 2:
        return "Тупоугольный треугольник"
    else:
        return "Остроугольный треугольник"


def calculate_triangle_area(a, b, c):
    if not check_triangle_sides(a, b, c):
        return None

    p = (a + b + c) / 2
    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    return area


def on_calculate():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        c = float(entry_c.get())

        triangle_type = determine_triangle_type(a, b, c)
        triangle_area = calculate_triangle_area(a, b, c)

        result_label.config(text=f"Вид треугольника: {triangle_type}\nПлощадь треугольника: {triangle_area}")
    except ValueError:
        result_label.config(text="Ошибка ввода. Пожалуйста, введите числовые значения.")


# Создание главного окна
root = tk.Tk()
root.title("Определение треугольника")

# Создание и размещение элементов интерфейса
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Сторона a:").grid(row=0, column=0, sticky=tk.W)
entry_a = ttk.Entry(frame)
entry_a.grid(row=0, column=1)

ttk.Label(frame, text="Сторона b:").grid(row=1, column=0, sticky=tk.W)
entry_b = ttk.Entry(frame)
entry_b.grid(row=1, column=1)

ttk.Label(frame, text="Сторона c:").grid(row=2, column=0, sticky=tk.W)
entry_c = ttk.Entry(frame)
entry_c.grid(row=2, column=1)

calculate_button = ttk.Button(frame, text="Рассчитать", command=on_calculate)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Запуск главного цикла
root.mainloop()