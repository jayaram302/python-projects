import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Basic Calculator")
root.geometry("350x450")
root.resizable(False, False)

# Variables
num1 = tk.StringVar()
num2 = tk.StringVar()
result = tk.StringVar()


# Calculate function
def calculate(operation):
    try:
        a = float(num1.get())
        b = float(num2.get())

        if operation == "+":
            answer = a + b
        elif operation == "-":
            answer = a - b
        elif operation == "*":
            answer = a * b
        elif operation == "/":
            if b == 0:
                messagebox.showerror("Error", "Cannot divide by zero")
                return
            answer = a / b

        result.set(str(answer))

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers"
        )


# Clear function
def clear():
    num1.set("")
    num2.set("")
    result.set("")


# Title
title = tk.Label(
    root,
    text="Basic Calculator",
    font=("Arial", 22, "bold")
)
title.pack(pady=20)

# First number
tk.Label(
    root,
    text="Enter First Number",
    font=("Arial", 12)
).pack()

tk.Entry(
    root,
    textvariable=num1,
    font=("Arial", 14),
    width=20
).pack(pady=8)

# Second number
tk.Label(
    root,
    text="Enter Second Number",
    font=("Arial", 12)
).pack()

tk.Entry(
    root,
    textvariable=num2,
    font=("Arial", 14),
    width=20
).pack(pady=8)

# Operation buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(
    button_frame,
    text="+",
    font=("Arial", 16, "bold"),
    width=5,
    command=lambda: calculate("+")
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="-",
    font=("Arial", 16, "bold"),
    width=5,
    command=lambda: calculate("-")
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="×",
    font=("Arial", 16, "bold"),
    width=5,
    command=lambda: calculate("*")
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="÷",
    font=("Arial", 16, "bold"),
    width=5,
    command=lambda: calculate("/")
).grid(row=0, column=3, padx=5)

# Result
tk.Label(
    root,
    text="Result",
    font=("Arial", 14, "bold")
).pack(pady=10)

tk.Entry(
    root,
    textvariable=result,
    font=("Arial", 16),
    width=20,
    state="readonly"
).pack()

# Clear button
tk.Button(
    root,
    text="CLEAR",
    font=("Arial", 12, "bold"),
    width=15,
    command=clear
).pack(pady=25)

# Start application
root.mainloop()