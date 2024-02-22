import tkinter as tk
import random

class NumberGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Генератор чисел до 100000")
        self.geometry("330x200")

        self.create_widgets()

    def create_widgets(self):
        self.generated_number_var = tk.StringVar()
        self.generated_number_var.set("")

        self.result_label = tk.Label(self, textvariable=self.generated_number_var, font=("Arial", 18))
        self.result_label.pack(pady=20)

        generate_button = tk.Button(self, text="Сгенерировать число", command=self.generate_number)
        generate_button.pack()

    def generate_number(self):
        random_number = random.randint(1, 100000)
        self.generated_number_var.set(str(random_number))

if __name__ == "__main__":
    app = NumberGeneratorApp()
    app.mainloop()
