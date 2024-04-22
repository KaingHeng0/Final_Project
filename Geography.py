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
# OPEN GEOGRAPHY WINDOW
def open_geo_window(username=None):
        geo_window = tk.Tk()
        geo_window.title('Geography Quiz')
    
        # Set window dimensions
        geo_window.geometry("600x400")

        # Title label
        title_label = tk.Label(geo_window, text="Welcome to the Geography Quiz", font=("Arial", 20, "bold"), pady=10)
        title_label.pack()
    
        # Instruction label
        instruction_label = tk.Label(geo_window, text="How many quizzes do you want to take? (Minimum: 2, Maximum: 20)", font=("Arial", 16))
        instruction_label.pack()
    
        # Entry box for number of quizzes
        quiz_entry = tk.Entry(geo_window, width=10, font=("Arial", 18))
        quiz_entry.pack(pady=5)
    
        # Press enter label
        press_enter_label = tk.Label(geo_window, text="Press Enter", font=("Arial", 12))
        press_enter_label.pack()

        # Return to category function
        def return_to_category(username):
            app_window = tk.Tk()
            application.open_application(username, app_window)
    
            geo_window.destroy()

        # Return to category button
        return_button = tk.Button(geo_window, text='Return', command=lambda: return_to_category(username))
        return_button.pack(side='bottom', pady=10)
    
        # Function to send message
        def send_message():
            message = quiz_entry.get()
            try:
                num_quizzes = int(message)
                if 2 <= num_quizzes <= 20:
                    label = tk.Label(geo_window, text=f"You selected to take {num_quizzes} quizzes.")
                    label.pack()
                    # Start quiz
                    start_quiz(geo_window, num_quizzes, username)
                else:
                    label = tk.Label(geo_window, text="Please enter a number between 2 and 20")
                    label.pack()
            except ValueError:
                label = tk.Label(geo_window, text="Please enter a valid number.")
                label.pack()
    
        # Bind function to entry box
        def on_entry(event=None):
            send_message()
    
        quiz_entry.bind("<Return>", on_entry)

        # RESOURCES_FUNCTION - geography
        def open_resources_window():
            resources_window = tk.Toplevel()
            resources_window.title("Geography Resources")
            resources_window.geometry('800x600')

            def open_national_geographic_kids():
                webbrowser.open_new("https://kids.nationalgeographic.com/")

            def open_world_atlas():
                webbrowser.open_new("https://www.worldatlas.com/")

            def open_geoguessr():
                webbrowser.open_new("https://geoguessr.com/")

            def open_geographyIQ():
                webbrowser.open_new("https://www.geographyiq.com/")

            def open_google_earth():
                webbrowser.open_new("https://www.google.com/earth/")

            # Close geography resources window
            def close_geography(resources_window):

                # Close the resources window
                resources_window.destroy()

            return_to_python_btn = tk.Button(resources_window, text='Close',command=lambda: close_geography(resources_window))
            return_to_python_btn.pack(pady=10, side='bottom')

            descriptions = {
                "National Geographic Kids": "National Geographic Kids offers educational resources, games, and videos to inspire young \n"
                                            "learners to explore the world.",
                "World Atlas": "World Atlas is an online resource providing maps, geographical information, and educational \n"
                               "tools for learning about countries, continents, and regions worldwide.",
                "GeoGuesser": "GeoGuessr is an online geography game that uses Google Street View to challenge players to guess\n"
                              " the locations of random street views from around the world.",
                "GeographyIQ": "GeographyIQ provides comprehensive geographic information, including maps, statistics, and facts \n"
                               "about countries and regions worldwide.",
                "Google Earth": "Google Earth allows users to explore the world through satellite imagery, maps, terrain,\n"
                                " 3D buildings, and more."
            }

            for name, url in [("National Geographic Kids", open_national_geographic_kids),
                              ("World Atlas", open_world_atlas),
                              ("GeoGuesser", open_geoguessr),
                              ("GeographyIQ", open_geographyIQ),
                              ("Google Earth", open_google_earth)]:
                description_label = tk.Label(resources_window, text=descriptions[name])
                description_label.pack(pady=(10,2))
                btn = tk.Button(resources_window, text=name, command=url)
                btn.pack(pady=(2,15))

        # Resources button
        resources_btn = tk.Button(geo_window, text='Geography Recourses', command=open_resources_window)
        resources_btn.pack(side='bottom', pady=10, before=return_button)
    
        # Display the window
        geo_window.mainloop()

# Define the quiz questions, options, and correct answers
quiz_data = {
    "Capital of Canada": {
        "options": ["Toronto", "Montreal", "Vancouver", "Ottawa"],
        "correct_answer": "Ottawa"
    },
    "Largest ocean by surface area": {
        "options": ["Atlantic Ocean", "Indian Ocean", "Southern Ocean", "Pacific Ocean"],
        "correct_answer": "Pacific Ocean"
    },
    "Tallest mountain in the world": {
        "options": ["K2", "Kangchenjunga", "Mount Kilimanjaro", "Mount Everest"],
        "correct_answer": "Mount Everest"
    },
    "Largest desert in the world": {
        "options": ["Gobi Desert", "Arabian Desert", "Kalahari Desert", "Sahara Desert"],
        "correct_answer": "Sahara Desert"
    },
    "Capital of Brazil": {
        "options": ["Rio de Janeiro", "São Paulo", "Salvador", "Brasília"],
        "correct_answer": "Brasília"
    },
    "Capital of Australia": {
        "options": ["Sydney", "Melbourne", "Brisbane", "Canberra"],
        "correct_answer": "Canberra"
    },
    "Largest river in South America": {
        "options": ["Amazon River", "Orinoco River", "Paraná River", "Magdalena River"],
        "correct_answer": "Amazon River"
    },
    "Currency of Russia": {
        "options": ["Euro", "Ruble", "Yen", "Pound"],
        "correct_answer": "Ruble"
    },
    "Deepest point in the ocean": {
        "options": ["Marianas Trench", "Puerto Rico Trench", "Tonga Trench", "Philippine Trench"],
        "correct_answer": "Marianas Trench"
    },
    "Country with the largest population": {
        "options": ["United States", "India", "China", "Brazil"],
        "correct_answer": "China"
    },
    "Longest reigning British monarch": {
        "options": ["Queen Elizabeth I", "Queen Victoria", "Queen Elizabeth II", "King George III"],
        "correct_answer": "Queen Elizabeth II"
    },
    "Largest island in the Mediterranean Sea": {
        "options": ["Sicily", "Sardinia", "Cyprus", "Crete"],
        "correct_answer": "Sicily"
    },
    "Capital of South Africa": {
        "options": ["Johannesburg", "Pretoria", "Cape Town", "Durban"],
        "correct_answer": "Pretoria"
    },
    "Country with the largest number of UNESCO World Heritage Sites": {
        "options": ["Italy", "China", "Mexico", "France"],
        "correct_answer": "Italy"
    },
    "Longest border between two countries": {
        "options": ["Canada-USA border", "China-Russia border", "Brazil-Argentina border", "India-Pakistan border"],
        "correct_answer": "Canada-USA border"
    },
    "Deepest lake in the world": {
        "options": ["Lake Baikal", "Lake Superior", "Lake Tanganyika", "Crater Lake"],
        "correct_answer": "Lake Baikal"
    },
    "Largest continent by land area": {
        "options": ["Africa", "North America", "Europe", "Asia"],
        "correct_answer": "Asia"
    },
    "Longest river in the world": {
        "options": ["Amazon River", "Mississippi River", "Yangtze River", "Nile River"],
        "correct_answer": "Nile River"
    },
    "Highest mountain peak in North America": {
        "options": ["Mount Everest", "Mount Kilimanjaro", "Mount Whitney", "Denali (formerly Mount McKinley)"],
        "correct_answer": "Denali (formerly Mount McKinley)"
    },
    "Country known as the 'Land of the Rising Sun'": {
        "options": ["China", "South Korea", "Vietnam", "Japan"],
        "correct_answer": "Japan"
    }
}


# START QUIZ WINDOW
def start_quiz(geo_window, num_quizzes, username):
    global score
    score = 0
    # Shuffle the keys (questions) to randomize quiz order
    questions = list(quiz_data.keys())
    random.shuffle(questions)

    # Display the first question
    display_question(geo_window, questions, 0, num_quizzes, username)

# SCORE CALCULATION
def calculate_result(score, total_questions):
    score_number = f"{score}"
    percentage = f"{(score / total_questions) * 100:.2f}%"
    return score_number, percentage

# MAIN FUNCTION
def display_question(geo_window, questions, current_question_index, num_quizzes, username):
    # Clear previous question frame if exists
    clear_frame(geo_window)

    # Get current question
    question = questions[current_question_index]
    options = quiz_data[question]["options"]
    correct_answer = quiz_data[question]["correct_answer"]

    # Create a frame for the question and options
    question_frame = tk.Frame(geo_window)
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
    button_command = (lambda: display_question(geo_window, questions, current_question_index + 1, num_quizzes, username)) if current_question_index < num_quizzes - 1 else (lambda: return_to_panel(username, score, num_quizzes, geo_window))
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
def return_to_panel(username, score, num_quizzes, geo_window):
    # Display quiz result
    display_quiz_result(username, score, num_quizzes, "Geography")

    # Retrieve and display previous quiz results
    previous_results = retrieve_quiz_results(username)
    print("Previous quiz results:")
    for result in previous_results:
        print(result)
    # Destroy the previous quiz panel
    geo_window.destroy()
    # Assuming open_geo_window() initializes the main page
    open_geo_window(username)

#CLEAR
def clear_frame(window):
    for widget in window.winfo_children():
        widget.destroy()
