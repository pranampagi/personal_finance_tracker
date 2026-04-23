import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from finance_manager import FinanceManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antigravity Finance Tracker")
        self.root.geometry("1100x700")
        
        self.manager = FinanceManager()
        
        # Define Colors
        self.colors = {
            "bg": "#f0f2f5",
            "sidebar": "#1e293b",
            "header": "#ffffff",
            "accent": "#3b82f6",
            "income": "#22c55e",
            "expense": "#ef4444",
            "text": "#334155"
        }
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_data()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure Treeview
        self.style.configure("Treeview", 
                           background="#ffffff",
                           foreground=self.colors["text"],
                           rowheight=30,
                           fieldbackground="#ffffff",
                           font=("Helvetica", 10))
        self.style.map("Treeview", background=[('selected', self.colors["accent"])])
        
        # Configure Buttons
        self.style.configure("Accent.TButton", 
                           foreground="white", 
                           background=self.colors["accent"],
                           font=("Helvetica", 10, "bold"))
        
        self.root.configure(bg=self.colors["bg"])

    def create_widgets(self):
        # Header / Summary Bar
        self.header = tk.Frame(self.root, bg=self.colors["header"], height=80, relief="flat")
        self.header.pack(side="top", fill="x", pady=(0, 10))
        
        self.summary_frame = tk.Frame(self.header, bg=self.colors["header"])
        self.summary_frame.pack(expand=True)
        
        self.balance_label = tk.Label(self.summary_frame, text="Balance: $0.00", font=("Helvetica", 18, "bold"), bg=self.colors["header"], fg=self.colors["text"])
        self.balance_label.pack(side="left", padx=30)
        
        self.income_label = tk.Label(self.summary_frame, text="Income: $0.00", font=("Helvetica", 14), bg=self.colors["header"], fg=self.colors["income"])
        self.income_label.pack(side="left", padx=20)
        
        self.expense_label = tk.Label(self.summary_frame, text="Expenses: $0.00", font=("Helvetica", 14), bg=self.colors["header"], fg=self.colors["expense"])
        self.expense_label.pack(side="left", padx=20)

        # Main Content
        self.content = tk.Frame(self.root, bg=self.colors["bg"])
        self.content.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Column: Add Transaction and History
        self.left_col = tk.Frame(self.content, bg=self.colors["bg"])
        self.left_col.pack(side="left", fill="both", expand=True)

        # Add Transaction Frame
        self.add_frame = tk.LabelFrame(self.left_col, text="Add Transaction", font=("Helvetica", 12, "bold"), bg="white", padx=15, pady=15)
        self.add_frame.pack(fill="x", pady=(0, 20))

        # Form Fields
        fields = [("Description:", "desc"), ("Amount:", "amount"), ("Category:", "cat")]
        self.entries = {}
        
        self.add_frame.columnconfigure(1, weight=1)
        for i, (label_text, key) in enumerate(fields):
            tk.Label(self.add_frame, text=label_text, bg="white", fg=self.colors["text"]).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(self.add_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            self.entries[key] = entry

        tk.Label(self.add_frame, text="Type:", bg="white", fg=self.colors["text"]).grid(row=3, column=0, sticky="w", pady=5)
        self.type_var = tk.StringVar(value="Expense")
        self.type_menu = ttk.Combobox(self.add_frame, textvariable=self.type_var, values=["Income", "Expense"], state="readonly")
        self.type_menu.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        self.add_btn = ttk.Button(self.add_frame, text="Save Transaction", command=self.add_transaction, style="Accent.TButton")
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=15)

        # History Table
        self.history_frame = tk.LabelFrame(self.left_col, text="Recent History", font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        self.history_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.history_frame, columns=("ID", "Date", "Description", "Category", "Type", "Amount"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Right Column: Charts
        self.right_col = tk.Frame(self.content, bg=self.colors["bg"], width=400)
        self.right_col.pack(side="right", fill="both", padx=(20, 0))

        self.chart_frame = tk.LabelFrame(self.right_col, text="Financial Visualization", font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        self.chart_frame.pack(fill="both", expand=True)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def add_transaction(self):
        desc = self.entries["desc"].get()
        amount_str = self.entries["amount"].get()
        cat = self.entries["cat"].get()
        t_type = self.type_var.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not desc or not amount_str or not cat:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number.")
            return

        if self.manager.add_entry(date, desc, cat, t_type, amount):
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self.refresh_data()
        else:
            messagebox.showerror("Error", "Failed to save transaction.")

    def refresh_data(self):
        # Update Summary
        summary = self.manager.get_summary()
        self.balance_label.config(text=f"Balance: ${summary['balance']:,.2f}")
        self.income_label.config(text=f"Income: ${summary['income']:,.2f}")
        self.expense_label.config(text=f"Expenses: ${summary['expense']:,.2f}")

        # Update History Table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.manager.get_history():
            self.tree.insert("", "end", values=row)

        # Update Charts
        self.update_charts()

    def update_charts(self):
        self.ax.clear()
        chart_data = self.manager.get_chart_data()
        
        expense_cats, expense_amounts = chart_data["expense_pie"]
        
        if expense_amounts and sum(expense_amounts) > 0:
            self.ax.pie(expense_amounts, labels=expense_cats, autopct='%1.1f%%', startangle=140, 
                        colors=['#3b82f6', '#22c55e', '#ef4444', '#f59e0b', '#8b5cf6', '#ec4899'])
            self.ax.set_title("Expenses by Category", fontsize=12, pad=20)
        else:
            self.ax.text(0.5, 0.5, "No expense data yet", ha='center', va='center')
            self.ax.set_title("Waiting for data...", fontsize=12)

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
