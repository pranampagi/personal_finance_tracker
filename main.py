import tkinter as tk
from src.ui.app import FinanceApp

def main():
    root = tk.Tk()
    # Style the root window
    root.configure(bg="#f8fafc")
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
