import tkinter as tk
from tkinter import messagebox
import sqlite3
import application

# Initialize SQLite connection and cursor
conn = sqlite3.connect('userdata.db')
cursor = conn.cursor()

# Create table to store user data if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')
conn.commit()

def register_user(login_window):
    def register():
        username = username_entry_reg.get()
        password = password_entry_reg.get()

        # Check if username is new
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")
            return

        # Check password length
        if not 8 <= len(password) <= 12:
            messagebox.showerror("Error", "Password must be between 8 and 12 characters long.")
            return

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        messagebox.showinfo("Success", "Registration successful!")

        # Closing register panel
        register_window.destroy()

    # Create registration window
    register_window = tk.Toplevel(login_window)
    register_window.title("Registration Page")

    # Create username label and entry field
    username_label_reg = tk.Label(register_window, text="Username:")
    username_label_reg.grid(row=0, column=0, padx=10, pady=5)
    username_entry_reg = tk.Entry(register_window)
    username_entry_reg.grid(row=0, column=1, padx=10, pady=5)

    # Create password label and entry field
    password_label_reg = tk.Label(register_window, text="Password:")
    password_label_reg.grid(row=1, column=0, padx=10, pady=5)
    password_entry_reg = tk.Entry(register_window, show="*")
    password_entry_reg.grid(row=1, column=1, padx=10, pady=5)

    # Create register button
    register_button = tk.Button(register_window, text="Register", command=register)
    register_button.grid(row=2, column=0, columnspan=2, pady=10)


def login(root):
    # Create login window
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    # Display welcome message
    welcome_label = tk.Label(login_window, text="Welcome to Quiz Application")
    welcome_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Create username label and entry field
    username_label = tk.Label(login_window, text="Username:")
    username_label.grid(row=1, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    # Create password label and entry field
    password_label = tk.Label(login_window, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    def login_command():
        username = username_entry.get()
        password = password_entry.get()

        # Check if username exists and password is correct
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login successful!")

            # Close login panel
            login_window.destroy()

            # Connect to application file
            application.open_application(username, root)

        else:
            messagebox.showerror("Error", "Incorrect username or password.")

    login_button = tk.Button(login_window, text="Login", command=login_command)
    login_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Create register link
    register_link = tk.Label(login_window, text="Register for new users", fg="blue", cursor="hand2")
    register_link.grid(row=4, column=0, columnspan=2, pady=5)
    register_link.bind("<Button-1>", lambda e: register_user(login_window))

    return login_window
