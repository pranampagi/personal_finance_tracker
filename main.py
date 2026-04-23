import tkinter as tk
from app import FinanceApp

def main():
    root = tk.Tk()
    # Set icon if available (optional)
    # root.iconbitmap('icon.ico') 
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
