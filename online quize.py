import tkinter as tk
from tkinter import messagebox
import random

# -----------------------------
# Main Window FIRST
# -----------------------------
root = tk.Tk()
root.title("Online Quiz Platform")
root.geometry("600x500")
root.resizable(False, False)

# -----------------------------
# Variables
# -----------------------------
current_question = 0
score = 0

# StringVar must be created AFTER Tk()
selected_answer = tk.StringVar()

# -----------------------------
# Quiz Questions
# -----------------------------
questions = [
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "New Delhi", "Chennai", "Hyderabad"],
        "answer": "New Delhi"
    },
    {
        "question": "Which language is commonly used for Data Science?",
        "options": ["Python", "HTML", "CSS", "XML"],
        "answer": "Python"
    },
    {
        "question": "What is 10 + 20?",
        "options": ["20", "25", "30", "40"],
        "answer": "30"
    },
    {
        "question": "Which data structure follows FIFO?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "answer": "Queue"
    },
    {
        "question": "Which of these is a database?",
        "options": ["MySQL", "Python", "HTML", "CSS"],
        "answer": "MySQL"
    }
]

random.shuffle(questions)

# -----------------------------
# Title
# -----------------------------
title = tk.Label(
    root,
    text="ONLINE QUIZ PLATFORM",
    font=("Arial", 24, "bold")
)

title.pack(pady=20)

# -----------------------------
# Question Number
# -----------------------------
question_number = tk.Label(
    root,
    text="",
    font=("Arial", 13)
)

question_number.pack(pady=5)

# -----------------------------
# Question
# -----------------------------
question_label = tk.Label(
    root,
    text="",
    font=("Arial", 17, "bold"),
    wraplength=500
)

question_label.pack(pady=20)

# -----------------------------
# Answer Options
# -----------------------------
options = []

for i in range(4):

    option = tk.Radiobutton(
        root,
        text="",
        variable=selected_answer,
        value="",
        font=("Arial", 13)
    )

    options.append(option)

    option.pack(
        anchor="w",
        padx=50,
        pady=5
    )

# -----------------------------
# Show Question
# -----------------------------
def show_question():

    selected_answer.set("")

    question_data = questions[current_question]

    question_number.config(
        text=f"Question {current_question + 1} of {len(questions)}"
    )

    question_label.config(
        text=question_data["question"]
    )

    for i in range(4):

        options[i].config(
            text=question_data["options"][i],
            value=question_data["options"][i]
        )


# -----------------------------
# Next Question
# -----------------------------
def next_question():

    global current_question
    global score

    answer = selected_answer.get()

    if answer == "":
        messagebox.showwarning(
            "Warning",
            "Please select an answer!"
        )
        return

    correct_answer = questions[current_question]["answer"]

    if answer == correct_answer:
        score += 1

    current_question += 1

    if current_question < len(questions):

        show_question()

    else:

        show_result()


# -----------------------------
# Show Result
# -----------------------------
def show_result():

    percentage = (score / len(questions)) * 100

    question_number.config(
        text="QUIZ COMPLETED!"
    )

    question_label.config(
        text=f"Your Score: {score}/{len(questions)}\n\n"
             f"Percentage: {percentage:.1f}%"
    )

    for option in options:
        option.pack_forget()

    next_button.pack_forget()

    restart_button.pack(pady=20)


# -----------------------------
# Restart Quiz
# -----------------------------
def restart_quiz():

    global current_question
    global score

    current_question = 0
    score = 0

    random.shuffle(questions)

    for option in options:

        option.pack(
            anchor="w",
            padx=50,
            pady=5
        )

    restart_button.pack_forget()

    next_button.pack(pady=20)

    show_question()


# -----------------------------
# Next Button
# -----------------------------
next_button = tk.Button(
    root,
    text="NEXT QUESTION",
    font=("Arial", 13, "bold"),
    width=20,
    command=next_question
)

next_button.pack(pady=20)

# -----------------------------
# Restart Button
# -----------------------------
restart_button = tk.Button(
    root,
    text="RESTART QUIZ",
    font=("Arial", 13, "bold"),
    width=20,
    command=restart_quiz
)

# -----------------------------
# Start Quiz
# -----------------------------
show_question()

# Start Tkinter
root.mainloop()