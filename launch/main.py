import tkinter as tk
import os

class LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Desktop Лаунчер")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Выберите программу для запуска:", font=("Arial", 12)).pack(pady=10)

        calculator_button = tk.Button(self, text="Калькулятор", command=self.run_calculator)
        calculator_button.pack()

        snake_game_button = tk.Button(self, text="Игра Змейка", command=self.run_snake_game)
        snake_game_button.pack()

        number_generator_button = tk.Button(self, text="Генератор чисел до 100000", command=self.run_number_generator)
        number_generator_button.pack()

    def run_calculator(self):
        os.system("python calculator.py")

    def run_snake_game(self):
        os.system("python snake_game.py")

    def run_number_generator(self):
        os.system("python number_generator.py")

if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
