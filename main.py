import tkinter as tk
import login


# Create main window
root = tk.Tk()
root.withdraw()


# Call the login function from login.py to display the login panel
login_window = login.login(root)

login_window.mainloop()
