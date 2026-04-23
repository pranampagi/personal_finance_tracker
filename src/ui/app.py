import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from src.core.finance_manager import FinanceManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Try to use ttkbootstrap for modern UI
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    BOOTSTRAP_AVAILABLE = True
except ImportError:
    from tkinter import ttk
    BOOTSTRAP_AVAILABLE = False

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aura Finance - Personal Tracker")
        self.root.geometry("1200x800")
        
        self.manager = FinanceManager()
        
        # Currency Symbol
        self.currency = "₹"
        
        # Modern Color Palette
        self.colors = {
            "bg": "#f8fafc",
            "sidebar": "#1e293b",
            "header": "#ffffff",
            "accent": "#0ea5e9",
            "income": "#10b981",
            "expense": "#f43f5e",
            "text": "#334155"
        }
        
        if not BOOTSTRAP_AVAILABLE:
            self.setup_custom_styles()
        else:
            # If bootstrap is available, we can use a theme
            self.style = ttk.Style(theme="flatly")
        
        self.create_widgets()
        self.refresh_data()

    def setup_custom_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("Treeview", 
                           background="#ffffff",
                           foreground=self.colors["text"],
                           rowheight=35,
                           fieldbackground="#ffffff",
                           font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", background=[('selected', self.colors["accent"])])
        
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        self.style.configure("Accent.TButton", background=self.colors["accent"], foreground="white")
        
        self.root.configure(bg=self.colors["bg"])

    def create_widgets(self):
        # Header Section
        self.header = tk.Frame(self.root, bg=self.colors["header"], height=100, relief="flat", highlightbackground="#e2e8f0", highlightthickness=1)
        self.header.pack(side="top", fill="x", pady=(0, 20))
        
        header_content = tk.Frame(self.header, bg=self.colors["header"])
        header_content.pack(expand=True, fill="both", padx=40)
        
        # Logo/Title
        title_frame = tk.Frame(header_content, bg=self.colors["header"])
        title_frame.pack(side="left")
        tk.Label(title_frame, text="Aura Finance", font=("Segoe UI", 24, "bold"), bg=self.colors["header"], fg=self.colors["accent"]).pack(anchor="w")
        tk.Label(title_frame, text="Smart Tracking • Better Savings", font=("Segoe UI", 9), bg=self.colors["header"], fg="#94a3b8").pack(anchor="w")

        # Summary Cards
        summary_container = tk.Frame(header_content, bg=self.colors["header"])
        summary_container.pack(side="right", fill="y")
        
        self.balance_val = tk.Label(summary_container, text=f"{self.currency}0", font=("Segoe UI", 20, "bold"), bg=self.colors["header"], fg=self.colors["text"])
        self.balance_val.pack(side="right", padx=20)
        tk.Label(summary_container, text="Net Balance", font=("Segoe UI", 9, "bold"), bg=self.colors["header"], fg="#64748b").pack(side="right")

        # Main Layout: Two Columns
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(fill="both", expand=True, padx=40)

        # Left: Form & Stats
        self.left_panel = tk.Frame(self.main_container, bg=self.colors["bg"])
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Stats Cards (Income/Expense Small Cards)
        stats_frame = tk.Frame(self.left_panel, bg=self.colors["bg"])
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Income Card
        inc_card = tk.Frame(stats_frame, bg="white", padx=15, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
        inc_card.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(inc_card, text="TOTAL INCOME", font=("Segoe UI", 8, "bold"), bg="white", fg="#64748b").pack(anchor="w")
        self.income_val = tk.Label(inc_card, text=f"{self.currency}0", font=("Segoe UI", 14, "bold"), bg="white", fg=self.colors["income"])
        self.income_val.pack(anchor="w")

        # Expense Card
        exp_card = tk.Frame(stats_frame, bg="white", padx=15, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
        exp_card.pack(side="left", fill="x", expand=True, padx=(10, 0))
        tk.Label(exp_card, text="TOTAL EXPENSES", font=("Segoe UI", 8, "bold"), bg="white", fg="#64748b").pack(anchor="w")
        self.expense_val = tk.Label(exp_card, text=f"{self.currency}0", font=("Segoe UI", 14, "bold"), bg="white", fg=self.colors["expense"])
        self.expense_val.pack(anchor="w")

        # Input Form
        form_frame = tk.Frame(self.left_panel, bg="white", padx=25, pady=25, highlightbackground="#e2e8f0", highlightthickness=1)
        form_frame.pack(fill="x")
        
        tk.Label(form_frame, text="Add New Transaction", font=("Segoe UI", 12, "bold"), bg="white", fg=self.colors["text"]).pack(anchor="w", pady=(0, 15))
        
        self.entries = {}
        fields = [("Description", "desc"), ("Amount", "amount"), ("Category", "cat")]
        
        grid_frame = tk.Frame(form_frame, bg="white")
        grid_frame.pack(fill="x")
        grid_frame.columnconfigure(1, weight=1)
        
        for i, (label, key) in enumerate(fields):
            tk.Label(grid_frame, text=label, bg="white", fg="#64748b", font=("Segoe UI", 9)).grid(row=i, column=0, sticky="w", pady=8)
            entry = ttk.Entry(grid_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=(15, 0), pady=8)
            self.entries[key] = entry

        tk.Label(grid_frame, text="Type", bg="white", fg="#64748b", font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w", pady=8)
        self.type_var = tk.StringVar(value="Expense")
        type_menu = ttk.Combobox(grid_frame, textvariable=self.type_var, values=["Income", "Expense"], state="readonly")
        type_menu.grid(row=3, column=1, sticky="ew", padx=(15, 0), pady=8)

        self.save_btn = ttk.Button(form_frame, text="Save Transaction", command=self.add_transaction, style="Accent.TButton")
        self.save_btn.pack(fill="x", pady=(20, 0))

        # Right: History & Visuals
        self.right_panel = tk.Frame(self.main_container, bg=self.colors["bg"])
        self.right_panel.pack(side="right", fill="both", expand=True)

        # History Table
        table_container = tk.Frame(self.right_panel, bg="white", padx=1, pady=1, highlightbackground="#e2e8f0", highlightthickness=1)
        table_container.pack(fill="both", expand=True, pady=(0, 20))
        
        tk.Label(table_container, text="Transaction History", font=("Segoe UI", 11, "bold"), bg="white", fg=self.colors["text"], padx=15, pady=10).pack(anchor="w")

        columns = ("Date", "Description", "Category", "Type", "Amount")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings")
        
        column_widths = {"Date": 120, "Description": 180, "Category": 120, "Type": 100, "Amount": 100}
        for col in columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=column_widths[col], anchor="w")
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")

        # Action Buttons below table
        action_frame = tk.Frame(self.right_panel, bg=self.colors["bg"])
        action_frame.pack(fill="x", pady=(0, 20))
        
        self.del_btn = ttk.Button(action_frame, text="Delete Selected", command=self.delete_transaction)
        self.del_btn.pack(side="right")

        # Visualization
        chart_container = tk.Frame(self.right_panel, bg="white", padx=15, pady=15, highlightbackground="#e2e8f0", highlightthickness=1)
        chart_container.pack(fill="x")
        
        self.fig, self.ax = plt.subplots(figsize=(6, 3), dpi=100)
        self.fig.patch.set_facecolor('white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def add_transaction(self):
        desc = self.entries["desc"].get()
        amount_str = self.entries["amount"].get()
        cat = self.entries["cat"].get()
        t_type = self.type_var.get()
        date = datetime.now().strftime("%d %b %Y, %H:%M")

        if not desc or not amount_str or not cat:
            messagebox.showwarning("Input Error", "Please fill in all transaction details.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid numeric amount.")
            return

        if self.manager.add_entry(date, desc, cat, t_type, amount):
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self.refresh_data()
        else:
            messagebox.showerror("Error", "Could not save transaction to database.")

    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Selection", "Please select a transaction to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
            for item in selected:
                # The first column in DB is ID, but we didn't show it in tree.
                # I need to fetch the ID. I'll re-implement get_history to include ID but hide it.
                # Actually, let's just store ID in the Treeview values but hide it from display.
                values = self.tree.item(item, "values")
                # Wait, I need to know which ID it corresponds to.
                # I'll update refresh_data to store ID as the iid or in tags.
                trans_id = self.tree.item(item, "tags")[0]
                self.manager.delete_entry(trans_id)
            self.refresh_data()

    def refresh_data(self):
        summary = self.manager.get_summary()
        self.balance_val.config(text=f"{self.currency}{summary['balance']:,.2f}")
        self.income_val.config(text=f"{self.currency}{summary['income']:,.2f}")
        self.expense_val.config(text=f"{self.currency}{summary['expense']:,.2f}")

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.manager.get_history():
            # row: (id, date, desc, cat, type, amount)
            t_id, t_date, t_desc, t_cat, t_type, t_amt = row
            display_values = (t_date, t_desc, t_cat, t_type, f"{self.currency}{t_amt:,.2f}")
            self.tree.insert("", "end", values=display_values, tags=(t_id,))

        self.update_charts()

    def update_charts(self):
        self.ax.clear()
        chart_data = self.manager.get_chart_data()
        expense_cats, expense_amounts = chart_data["expense_pie"]
        
        if expense_amounts and sum(expense_amounts) > 0:
            wedges, texts, autotexts = self.ax.pie(
                expense_amounts, 
                labels=expense_cats, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=['#0ea5e9', '#10b981', '#f43f5e', '#f59e0b', '#8b5cf6', '#ec4899'],
                pctdistance=0.85
            )
            # Add a circle at the center to make it a donut chart
            centre_circle = plt.Circle((0,0), 0.70, fc='white')
            self.fig.gca().add_artist(centre_circle)
            
            plt.setp(autotexts, size=8, weight="bold", color="white")
            plt.setp(texts, size=8)
            self.ax.set_title("Expense Breakdown", fontsize=10, fontname="Segoe UI", weight="bold")
        else:
            self.ax.text(0.5, 0.5, "Add expenses to see visualization", ha='center', va='center', color="#94a3b8")
            self.ax.axis('off')

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
