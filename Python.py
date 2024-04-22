# Import necessary libraries
import tkinter as tk
import random
from tkinter import messagebox
import application
import sqlite3
import datetime
import webbrowser

### BACKEND START ###
# Connect to SQLite database
conn = sqlite3.connect('quiz_results.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
             username TEXT,
             score INTEGER,
             total_questions INTEGER,
             timestamp TEXT,
             source TEXT
             )''')

# Commit changes
conn.commit()

# Function to store quiz results
def store_quiz_result(username, score, total_questions, source):
    # Insert quiz result into the database
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO quiz_results VALUES (?, ?, ?, ?, ?)", (username, score, total_questions, timestamp, source))
    conn.commit()

# Function to retrieve quiz results
def retrieve_quiz_results(username):
    # Retrieve quiz results for a specific user
    c.execute("SELECT * FROM quiz_results WHERE username=?", (username,))
    results = c.fetchall()
    return results

### BACKEND END ###

#Veriable
score = 0

# OPEN PYTHON WINDOW
def open_py_window(username=None):
    py_window = tk.Tk()
    py_window.title('Python Quiz')

    # Set window dimensions
    py_window.geometry("600x400")

    # Title label
    title_label = tk.Label(py_window, text="Welcome to the Python Quiz", font=("Arial", 20, "bold"), pady=10)
    title_label.pack()

    # Instruction label
    instruction_label = tk.Label(py_window, text="How many quizzes do you want to take? (Minimum: 2, Maximum: 20)", font=("Arial", 16))
    instruction_label.pack()

    # Entry box for number of quizzes
    quiz_entry = tk.Entry(py_window, width=10, font=("Arial", 18))
    quiz_entry.pack(pady=5)

    # Press enter label
    press_enter_label = tk.Label(py_window, text="Press Enter", font=("Arial", 12))
    press_enter_label.pack()

    # Return to category function
    def return_to_category(username):
        app_window = tk.Tk()
        application.open_application(username, app_window)

        py_window.destroy()

    # Return to category button
    return_button = tk.Button(py_window, text='Return', command=lambda: return_to_category(username))
    return_button.pack(side='bottom', pady=5)

    # Function to send message
    def send_message():
        message = quiz_entry.get()
        try:
            num_quizzes = int(message)
            if 2 <= num_quizzes <= 20:
                label = tk.Label(py_window, text=f"You selected to take {num_quizzes} quizzes.")
                label.pack()
                # Start quiz
                start_quiz(py_window, num_quizzes, username)
            else:
                label = tk.Label(py_window, text="Please enter a number between 2 and 20.")
                label.pack()
        except ValueError:
            label = tk.Label(py_window, text="Please enter a valid number.")
            label.pack()

    # Bind function to entry box
    def on_entry(event=None):
        send_message()

    quiz_entry.bind("<Return>", on_entry)


    #RESOURCES_FUNCTION - python
    def open_resources_window():
        resources_window = tk.Toplevel()
        resources_window.title("Python Resources")
        resources_window.geometry('600x500')

        def open_python_org():
            webbrowser.open_new("https://www.python.org/")

        def open_stackoverflow():
            webbrowser.open_new("https://stackoverflow.com/")

        def open_github():
            webbrowser.open_new("https://github.com/")

        def open_pypi():
            webbrowser.open_new("https://pypi.org/")

        def open_realpython():
            webbrowser.open_new("https://realpython.com/")

        # Close geography resources window
        def close_python(resources_window):

            # Close the resources window
            resources_window.destroy()

        return_to_python_btn = tk.Button(resources_window, text='Close', command=lambda: close_python(resources_window))
        return_to_python_btn.pack(pady=10, side='bottom')

        descriptions = {
            "Python.org": "The official website of the Python programming language.",
            "Stack Overflow": "A community-driven question and answer site for programming-related topics.",
            "GitHub": "A platform for hosting and collaborating on code repositories.",
            "PyPi": "The official repository for Python packages.",
            "Real Python": "An online platform offering tutorials, articles, and resources for Python developers."
        }

        for name, url in [("Python.org", open_python_org),
                          ("Stack Overflow", open_stackoverflow),
                          ("GitHub", open_github),
                          ("PyPi", open_pypi),
                          ("Real Python", open_realpython)]:
            description_label = tk.Label(resources_window, text=descriptions[name])
            description_label.pack(pady=(7,2))
            btn = tk.Button(resources_window, text=name, command=url)
            btn.pack(pady=(2,15))

    # Resources button
    resources_btn = tk.Button(py_window, text='Python Recourses', command=open_resources_window)
    resources_btn.pack(side='bottom', pady=10, before=return_button)

    # Display the window
    py_window.mainloop()

# Define the quiz questions, options, and correct answers
quiz_data = {
    "Which of the following is used to declare a variable in Python?": {
        "options": ["var", "let", "variable", "None of the above"],
        "correct_answer": "None of the above"
    },
    "What will the output of the following code be?\nprint(2 + 2 * 3)": {
        "options": [
            "8",
            "10",
            "12",
            "14"
        ],
        "correct_answer": "8"
    },
    "What is the purpose of the 'if' statement in Python?": {
        "options": ["To iterate over a sequence", "To define a function","To execute code conditionally",
                    "To perform arithmetic operations"
        ],
        "correct_answer":  "To execute code conditionally"
    },
    "Which of the following data types is mutable in Python?": {
            "options": ["Integer", "String", "Tuple", "List"],
            "correct_answer": "List"
        },
    "What will be the output of the following code?\nmy_list = [1, 2, 3, 4, 5]\nprint(my_list[1:3])": {
        "options": ["[1, 2]", "[2, 3]", "[2, 3, 4]", "[3, 4]"],
        "correct_answer": "[2, 3, 4]"
    },
    "Which keyword is used for function declaration in Python?": {
        "options": ["func", "def", "define", "function"],
        "correct_answer": "def"
    },
    "What does the 'import' keyword do in Python?": {
        "options": ["Exports variables from a module", "Imports modules or specific objects from modules",
                    "Defines a new class", "None of the above"],
        "correct_answer": "Imports modules or specific objects from modules"
    },
    "What does the 'pass' statement do in Python?": {
        "options": ["Terminates the program", "Skips the current block of code without executing anything",
                    "Raises an exception", "None of the above"],
        "correct_answer": "Skips the current block of code without executing anything"
    },
    "What will be the result of the following expression?\n3 * 'abc'": {
        "options": ["'abcabcabc'", "'aaabbbccc'", "'abcabc'", "Error"],
        "correct_answer": "'abcabcabc'"
    },
    "What is the output of the following code?\nprint(10 // 3)": {
        "options": ["3", "3.333", "3.0", "3.34"],
        "correct_answer": "3"
    },
    "What does the 'yield' keyword do in Python?": {
        "options": [
            "Returns a value from a function",
            "Pauses the execution of a function and returns a generator",
            "Terminates the execution of a function",
            "Defines a new class"
        ],
        "correct_answer": "Pauses the execution of a function and returns a generator"
    },
    "What is the purpose of the 'lambda' keyword in Python?": {
        "options": [
            "To declare anonymous functions",
            "To create a new instance of a class",
            "To define a generator function",
            "To perform matrix operations"
        ],
        "correct_answer": "To declare anonymous functions"
    },
    "What is the output of the following code?\nprint(isinstance(3, object))": {
        "options": ["True", "False", "3", "None"],
        "correct_answer": "True"
    },
    "What does the 'zip()' function do in Python?": {
        "options": [
            "Creates a zip file containing specified files",
            "Combines multiple iterables element-wise into tuples",
            "Unzips a file",
            "Converts a string to a zip object"
        ],
        "correct_answer": "Combines multiple iterables element-wise into tuples"
    },
    "What is the purpose of the 'with' statement in Python?": {
        "options": [
            "To declare a context manager",
            "To define a while loop",
            "To execute a block of code if a condition is true",
            "To define a for loop"
        ],
        "correct_answer": "To declare a context manager"
    },
    "What is the output of the following code?\nprint(*range(3))": {
        "options": ["[0, 1, 2]", "(0, 1, 2)", "0 1 2", "0\n1\n2"],
        "correct_answer": "0 1 2"
    },
    "What does the 'super()' function do in Python?": {
        "options": [
            "Returns the superclass of a class",
            "Calls a method in the superclass",
            "Creates a new instance of a class",
            "Terminates the execution of a method"
        ],
        "correct_answer": "Calls a method in the superclass"
    },
    "What is the purpose of the 'map()' function in Python?": {
        "options": [
            "Applies a function to each element of an iterable",
            "Creates a map object",
            "Filters elements of an iterable based on a function",
            "Combines multiple iterables element-wise into tuples"
        ],
        "correct_answer": "Applies a function to each element of an iterable"
    },
    "What is the output of the following code?\nprint(list(filter(lambda x: x > 2, [1, 2, 3, 4])))": {
        "options": ["[1, 2, 3, 4]", "[3, 4]", "[1, 2]", "[2, 3, 4]"],
        "correct_answer": "[3, 4]"
    },
    "What does the 'exec()' function do in Python?": {
        "options": [
            "Executes a block of code",
            "Exports variables from a module",
            "Imports modules or specific objects from modules",
            "Terminates the execution of a function"
        ],
        "correct_answer": "Executes a block of code"
    }
}

# START QUIZ WINDOW
def start_quiz(py_window, num_quizzes, username):
    global score
    score = 0
    # Shuffle the keys (questions) to randomize quiz order
    questions = list(quiz_data.keys())
    random.shuffle(questions)

    # Display the first question
    display_question(py_window, questions, 0, num_quizzes, username)

# SCORE CALCULATION
def calculate_result(score, total_questions):
    score_number = f"{score}"
    percentage = f"{(score / total_questions) * 100:.2f}%"
    return score_number, percentage

# MAIN FUNCTION
def display_question(py_window, questions, current_question_index, num_quizzes, username):
    # Clear previous question frame if exists
    clear_frame(py_window)

    # Get current question
    question = questions[current_question_index]
    options = quiz_data[question]["options"]
    correct_answer = quiz_data[question]["correct_answer"]

    # Create a frame for the question and options
    question_frame = tk.Frame(py_window)
    question_frame.pack(side="bottom", pady=20)

    # Title label for the current question
    title_label = tk.Label(question_frame, text=f"Question {current_question_index + 1}", font=("Arial", 20, "bold"))
    title_label.pack()

    # Label to display the question
    question_label = tk.Label(question_frame, text=question, font=("Arial", 16))
    question_label.pack(pady=10)

    # Shuffle the options to randomize their order
    random.shuffle(options)

    # Check score, radio, and result
    def check_answer():
        global score
        selected_answer = var.get()
        if selected_answer == correct_answer:
            result_label.config(text="Correct!")
            score += 1
        elif selected_answer == "":
            result_label.config(text="You missed this question.")
        else:
            result_label.config(text=f"Incorrect. The correct answer is: {correct_answer}")

        disable_radio_buttons()
        submit_button.config(state="disabled")
        next_button.config(state="normal")  # Enable next button after submitting answer

    def disable_radio_buttons():
        for widget in question_frame.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state="disabled")

    var = tk.StringVar()
    radio_buttons = []  # Store radio buttons in a list to disable them later

    for option in options:
        radio_button = tk.Radiobutton(question_frame, text=option, variable=var, value=option, font=("Arial", 14))
        radio_button.pack(anchor="w")
        radio_buttons.append(radio_button)

    # Submit button
    submit_button = tk.Button(question_frame, text="Submit", command=check_answer, font=("Arial", 16))
    submit_button.pack(pady=(10, 5))  # Adjusted padding

    # Label to display result
    result_label = tk.Label(question_frame, text="", font=("Arial", 14))
    result_label.pack()

    # Next button or Return button if it's the last question
    button_text = "Next" if current_question_index < num_quizzes - 1 else "Show result/Return"
    button_command = (lambda: display_question(py_window, questions, current_question_index + 1, num_quizzes, username)) if current_question_index < num_quizzes - 1 else (lambda: return_to_panel(username, score, num_quizzes, py_window))
    next_button = tk.Button(question_frame, text=button_text, command=button_command, font=("Arial", 16))
    next_button.pack(pady=20)

#DISPALY QUIC RESULT
def display_quiz_result(username, score, total_questions, source):
    # Store quiz result in the database
    store_quiz_result(username, score, total_questions, source)
    # Calculate the result
    score_number, percentage = calculate_result(score, total_questions)

    # Prepare the result message
    result_text = f"Score: {score_number} correct of {total_questions}\nPercentage: {percentage}, source: {source}"

    # Retrieve and display previous quiz results
    previous_results = retrieve_quiz_results(username)
    print("Previous quiz results:")
    for result in previous_results:
        print(result)

    # Show the result in a messagebox
    messagebox.showerror("Quiz result", result_text)

#RETURN TO APPLICATION FILE
def return_to_panel(username, score, num_quizzes, py_window):
    # Display quiz result
    display_quiz_result(username, score, num_quizzes, "Python")

    # Retrieve and display previous quiz results
    previous_results = retrieve_quiz_results(username)
    print("Previous quiz results:")
    for result in previous_results:
        print(result)
    # Destroy the previous quiz panel
    py_window.destroy()
    # Assuming open_py_window() initializes the main page
    open_py_window(username)

#CLEAR
def clear_frame(window):
    for widget in window.winfo_children():
        widget.destroy()

