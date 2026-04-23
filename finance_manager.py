from database import Database

class FinanceManager:
    def __init__(self, db_path="finance.db"):
        self.db = Database(db_path)

    def add_entry(self, date, description, category, trans_type, amount):
        """Add a new entry and return success."""
        try:
            self.db.add_transaction(date, description, category, trans_type, amount)
            return True
        except Exception as e:
            print(f"Error adding entry: {e}")
            return False

    def get_summary(self):
        """Get balance, total income, and total expense."""
        summary = self.db.get_summary_by_type()
        income = summary.get('Income', 0.0)
        expense = summary.get('Expense', 0.0)
        balance = income - expense
        return {
            "balance": balance,
            "income": income,
            "expense": expense
        }

    def get_history(self):
        """Get all transactions formatted for display."""
        return self.db.get_all_transactions()

    def get_chart_data(self):
        """Get data formatted for Matplotlib charts."""
        # For Pie Chart (Expense Categories)
        expense_breakdown = self.db.get_category_breakdown("Expense")
        categories = [item[0] for item in expense_breakdown]
        amounts = [item[1] for item in expense_breakdown]

        # For Bar Chart (Income vs Expense)
        summary = self.db.get_summary_by_type()
        types = list(summary.keys())
        totals = list(summary.values())

        return {
            "expense_pie": (categories, amounts),
            "summary_bar": (types, totals)
        }

    def delete_entry(self, trans_id):
        """Delete an entry."""
        self.db.delete_transaction(trans_id)

    def close(self):
        """Close connection."""
        self.db.close()
