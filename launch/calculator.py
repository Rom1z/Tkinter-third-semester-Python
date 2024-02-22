import tkinter as tk

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор")
        self.geometry("300x400")

        self.create_widgets()

    def create_widgets(self):
        self.result_var = tk.StringVar()

        entry = tk.Entry(self, textvariable=self.result_var, font=("Arial", 18), bd=10, justify="right")
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(self, text=text, font=("Arial", 18), bd=5, command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def on_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except Exception as e:
                self.result_var.set("Ошибка")
        else:
            current_text = self.result_var.get()
            if current_text == "Ошибка":
                current_text = ""
            self.result_var.set(current_text + char)

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
