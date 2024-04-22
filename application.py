import tkinter as tk
import Geography
import Python
import English

def open_application(username, root):
    # Close the login window
    root.destroy()

    # Open the application window
    app_window = tk.Tk()
    app_window.title('Quiz Application')

    # Set custom width and height
    app_window.geometry("400x300")  # Set width to 400 pixels and height to 300 pixels

    # Configure the columns and rows to expand vertically and horizontally
    app_window.columnconfigure(0, weight=1)
    app_window.rowconfigure(0, weight=1)
    app_window.rowconfigure(1, weight=1)
    app_window.rowconfigure(2, weight=1)
    app_window.rowconfigure(3, weight=1)

    # Welcome label (biggest)
    welcome_label = tk.Label(app_window, text='Welcome ' + username + ' to Quiz Application', font=("Arial", 20, "bold"), pady=20)
    welcome_label.grid(row=0, column=0, columnspan=3)

    # Instruction label (a bit smaller)
    message = tk.Label(app_window, text='Please choose one:', font=("Arial", 18))
    message.grid(row=1, column=0, columnspan=3, sticky="nsew")

    # Create a button for Geography
    geo_button = tk.Button(app_window, text="Geography", command=lambda: open_geo_window(username, app_window))
    geo_button.grid(row=2, column=0, padx=20, pady=5)

    # Create a button for Python
    python_button = tk.Button(app_window, text="Python", command=lambda: open_py_window(username, app_window))
    python_button.grid(row=2, column=1, padx=20, pady=5)

    # Create a button for English
    english_button = tk.Button(app_window, text="English", command = lambda : open_eng_window(username, app_window))
    english_button.grid(row=2, column=2, padx=20, pady=5)

    # Create a button for History
    history_button = tk.Button(app_window, text="History", command=lambda: open_history_window(username, app_window))
    history_button.grid(row=3, column=0, columnspan=3, pady=5)

def open_history_window(username, app_window):


    # Close the application window
    app_window.destroy()

    # Open the History panel
    # Here, you need to implement the functionality to display the quiz history
    # You can create a new window or dialog box to show the history from the database

    # For example:
    history_window = tk.Tk()
    history_window.title("Quiz History")


    # Retrieve quiz history from the database
    results = Geography.retrieve_quiz_results(username)

    # Display the results in the history window
    for idx, result in enumerate(results):
        label = tk.Label(history_window, text=f"Quiz {idx + 1}: Score: {result[1]} / {result[2]}, Timestamp: {result[3]}, Source: {result[4]}")
        label.pack()

    # Add a button to return to the main application window
    return_button = tk.Button(history_window, text="Return to Application", command=lambda: return_to_application(username, history_window))
    return_button.pack(pady=10)

def return_to_application(username, history_window):
    # Close the history window
    history_window.destroy()

    root = tk.Tk()

    # Reopen the application window
    open_application(username, root)
    if tk._default_root:
        tk._default_root.deiconify()

def open_geo_window(username, app_window):
    # Close the application window
    app_window.destroy()



    # Open the Geography panel
    Geography.open_geo_window(username)

def open_py_window(username, app_window):
    # Close the application window
    app_window.destroy()

    # Open the Geography panel
    Python.open_py_window(username)

def open_eng_window(username, app_window):
#Close the application window
    app_window.destroy()
    # Open the Geography panel
    English.open_eng_window(username)
