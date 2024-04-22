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

#Variable
score = 0

# OPEN ENGLISH WINDOW
def open_eng_window(username=None):
    eng_window = tk.Tk()
    eng_window.title('English Quiz')

    # Set window dimensions
    eng_window.geometry("700x400")

    # Title label
    title_label = tk.Label(eng_window, text="Welcome to the English Quiz", font=("Arial", 20, "bold"), pady=10)
    title_label.pack()

    # Instruction label
    instruction_label = tk.Label(eng_window, text="How many quizzes do you want to take? (Minimum: 2, Maximum: 20)", font=("Arial", 16))
    instruction_label.pack()

    # Entry box for number of quizzes
    quiz_entry = tk.Entry(eng_window, width=10, font=("Arial", 18))
    quiz_entry.pack(pady=5)

    # press enter label
    press_enter_label = tk.Label(eng_window, text="Press Enter", font=("Arial", 12))
    press_enter_label.pack()

    # return to category function
    def return_to_category(username):
        app_window = tk.Tk()
        application.open_application(username, app_window)

        eng_window.destroy()

    # return to category button
    return_button = tk.Button(eng_window, text='Return', command=lambda: return_to_category(username))
    return_button.pack(side='bottom', pady=5)

    # Function to send message OR ERROR HANDLING
    def send_message():
        message = quiz_entry.get()
        try:
            num_quizzes = int(message)
            if 2 <= num_quizzes <= 20:
                label = tk.Label(eng_window, text=f"You selected to take {num_quizzes} quizzes.")
                label.pack()
                # Start quiz
                start_quiz(eng_window, num_quizzes, username)
            else:
                label = tk.Label(eng_window, text="Please enter a number between 2 and 20.")
                label.pack()
        except ValueError:
            label = tk.Label(eng_window, text="Please enter a valid number.")
            label.pack()

    # Bind function to entry box
    def on_entry(event=None):
        send_message()

    quiz_entry.bind("<Return>", on_entry)

    # RESOURCES_FUNCTION - english
    def open_resources_window():
        resources_window = tk.Toplevel()
        resources_window.title("English Resources")
        resources_window.geometry('800x550')

        def open_merriam_webster():
            webbrowser.open_new("https://www.merriam-webster.com/")

        def open_grammarly():
            webbrowser.open_new("https://grammarly.com/")

        def open_thesaurus():
            webbrowser.open_new("https://thesaurus.com/")

        def open_oxford_dictionaries():
            webbrowser.open_new("https://oxfordlearnersdictionaries.com")

        def open_writing_explained():
            webbrowser.open_new("https://writingexplained.org")

        #Close_function
        def close_python(resources_window):
            # Close the resources window
            resources_window.destroy()

        #Close_recourse_btn
        return_to_python_btn = tk.Button(resources_window, text='Close', command=lambda: close_python(resources_window))
        return_to_python_btn.pack(pady=10, side='bottom')

        descriptions = {
            "Merriam-Webster": "Merriam-Webster is a renowned English dictionary and language reference site that provides\n"
                               " definitions, pronunciations, and word origins.",
            "Grammarly": "Grammarly offers writing assistance tools such as grammar and spell check, style suggestions,\n"
                              " and plagiarism detection to help users improve their writing skills.",
            "Thesaurus": "Thesaurus.com is a comprehensive online thesaurus providing synonyms, antonyms, and word definitions \n"
                         "to enhance vocabulary and writing.",
            "Oxford Dictionaries": "Oxford Dictionaries offers authoritative English language resources, including dictionaries,\n"
                                   " grammar guides, and language usage tips.",
            "Writing Explained ": "An online resource providing clear explanations and examples to enhance writing skills, covering \n"
                                  "grammar, punctuation, and style."
        }

        for name, url in [("Merriam-Webster", open_merriam_webster),
                          ("Grammarly", open_grammarly),
                          ("Thesaurus", open_thesaurus),
                          ("Oxford Dictionaries", open_oxford_dictionaries),
                          ("Writing Explained ", open_writing_explained)]:
            description_label = tk.Label(resources_window, text=descriptions[name])
            description_label.pack(pady=(7,2))
            btn = tk.Button(resources_window, text=name, command=url)
            btn.pack(pady=(2,15))

    #RESOURCES_BTN
    resources_btn = tk.Button(eng_window, text='English Recourses', command=open_resources_window)
    resources_btn.pack(side='bottom', pady=10, before=return_button)

    # Display the window
    eng_window.mainloop()

quiz_data = {
    "What is the difference between 'its' and 'it's' in English grammar?": {
        "options": [
            "'Its' is a possessive pronoun, and 'it's' is a contraction of 'it is' or 'it has'.",
            "'Its' is a contraction of 'it is' or 'it has', and 'it's' is a possessive pronoun.",
            "Both are possessive pronouns.",
            "Both are contractions."
        ],
        "correct_answer": "'Its' is a possessive pronoun, and 'it's' is a contraction of 'it is' or 'it has'."
    },
    "What is the definition of the word 'ephemeral'?": {
        "options": [
            "Existing only in the imagination; not real or actual.",
            "Lasting for a very short time.",
            "Showing great attention to detail; very careful and precise.",
            "Capable of being touched or felt; tangible."
        ],
        "correct_answer": "Lasting for a very short time."
    },
    "Which of the following is a correct example of the past tense form of the verb 'eat'?": {
        "options": [
            "Eated",
            "Ate",
            "Eaten",
            "Eating"
        ],
        "correct_answer": "Ate"
    },
    "What is a synonym for the word 'conundrum'?": {
        "options": [
            "Solution",
            "Riddle",
            "Clarity",
            "Explanation"
        ],
        "correct_answer": "Riddle"
    },
    "What does the idiom 'hit the nail on the head' mean?": {
        "options": [
            "Accidentally striking a nail with a hammer.",
            "Missing the intended target.",
            "To describe something as extremely expensive.",
            "To describe exactly what is causing a situation or problem."
        ],
        "correct_answer": "To describe exactly what is causing a situation or problem."
    },
    "What is the correct plural form of 'child'?": {
        "options": [
            "Childrens",
            "Childs",
            "Childes",
            "Children"
        ],
        "correct_answer": "Children"
    },
    "What is the definition of the word 'superfluous'?": {
        "options": [
            "Essential or necessary.",
            "Lacking in variety or originality.",
            "Beyond what is required; unnecessary.",
            "Showing great attention to detail; very careful and precise."
        ],
        "correct_answer": "Beyond what is required; unnecessary."
    },
    "Which of the following is a correct example of the comparative form of the adjective 'big'?": {
        "options": [
            "More big",
            "Bigger",
            "Biggest",
            "Bigly"
        ],
        "correct_answer": "Bigger"
    },
    "What is a synonym for the word 'ubiquitous'?": {
        "options": [
            "Unobtrusive",
            "Limited",
            "Invasive",
            "Widespread"
        ],
        "correct_answer": "Widespread"
    },
    "What does the idiom 'barking up the wrong tree' mean?": {
        "options": [
            "Trying to climb a tree while barking.",
            "Pursuing a mistaken or misguided course of action.",
            "Achieving a difficult task effortlessly.",
            "Being in complete agreement with someone."
        ],
        "correct_answer": "Pursuing a mistaken or misguided course of action."
    },
    "What is the plural form of the word 'mouse' (referring to the computer device)?": {
        "options": [
            "Mouses",
            "Mices",
            "Mouse",
            "Mice"
        ],
        "correct_answer": "Mice"
    },
    "What is the definition of the word 'inexorable'?": {
        "options": [
            "Impossible to stop or prevent.",
            "Showing or feeling active opposition or hostility towards someone or something.",
            "Capable of being touched or felt; tangible.",
            "Liable to change."
        ],
        "correct_answer": "Impossible to stop or prevent."
    },
    "Which of the following is a correct example of the past tense form of the verb 'fall'?": {
        "options": [
            "Fallen",
            "Fell",
            "Falled",
            "Falling"
        ],
        "correct_answer": "Fell"
    },
    "What is a synonym for the word 'juxtapose'?": {
        "options": [
            "Combine",
            "Place side by side",
            "Remove",
            "Separate"
        ],
        "correct_answer": "Place side by side"
    },
    "What does the idiom 'back to the drawing board' mean?": {
        "options": [
            "Revising or reconsidering a plan or strategy.",
            "Working on an art project.",
            "Going back to the previous stage of a process.",
            "Returning to a simpler task."
        ],
        "correct_answer": "Revising or reconsidering a plan or strategy."
    }
}

# START QUIZ WINDOW
def start_quiz(eng_window, num_quizzes, username):
    global score
    score = 0
    # Shuffle the keys (questions) to randomize quiz order
    questions = list(quiz_data.keys())
    random.shuffle(questions)

    # Display the first question
    display_question(eng_window, questions, 0, num_quizzes, username)

# SCORE CALCULATION
def calculate_result(score, total_questions):
    score_number = f"{score}"
    percentage = f"{(score / total_questions) * 100:.2f}%"
    return score_number, percentage

# MAIN FUNCTION
def display_question(eng_window, questions, current_question_index, num_quizzes, username):
    # Clear previous question frame if exists
    clear_frame(eng_window)

    # Get current question
    question = questions[current_question_index]
    options = quiz_data[question]["options"]
    correct_answer = quiz_data[question]["correct_answer"]

    # Create a frame for the question and options
    question_frame = tk.Frame(eng_window)
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
    button_command = (lambda: display_question(eng_window, questions, current_question_index + 1, num_quizzes,
                                               username)) if current_question_index < num_quizzes - 1 else (
        lambda: return_to_panel(username, score, num_quizzes, eng_window))
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
def return_to_panel(username, score, num_quizzes, eng_window):
    # Display quiz result
    display_quiz_result(username, score, num_quizzes, "English")

    # Retrieve and display previous quiz results
    previous_results = retrieve_quiz_results(username)
    print("Previous quiz results:")
    for result in previous_results:
        print(result)
    # Destroy the previous quiz panel
    eng_window.destroy()
    # Assuming open_eng_window() initializes the main page
    open_eng_window(username)

#CLEAR
def clear_frame(window):
    for widget in window.winfo_children():
        widget.destroy()
