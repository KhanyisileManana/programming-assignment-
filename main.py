import tkinter as tk
from database import init_db
from gui.styles import apply_theme
from gui.login import LoginWindow


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Campus Resource Booking System")
        self.geometry("1000x650")

        # Apply the theme
        apply_theme(self)

        self.current_user = None

        # Initialize the database
        init_db()

        # Start on the login screen
        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        self.current_user = None
        # Open the login window (which handles its own register button)
        LoginWindow(self, None)


if __name__ == "__main__":
    app = App()
    app.mainloop()