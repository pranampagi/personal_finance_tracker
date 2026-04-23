import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name=None):
        if db_name is None:
            # Default to data folder relative to project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_name = os.path.join(base_dir, "data", "finance.db")
        
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create the transactions table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def add_transaction(self, date, description, category, trans_type, amount):
        """Add a new transaction to the database."""
        self.cursor.execute('''
            INSERT INTO transactions (date, description, category, type, amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, description, category, trans_type, amount))
        self.conn.commit()

    def get_all_transactions(self):
        """Fetch all transactions sorted by date."""
        self.cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
        return self.cursor.fetchall()

    def get_summary_by_type(self):
        """Get totals for Income and Expense."""
        self.cursor.execute('SELECT type, SUM(amount) FROM transactions GROUP BY type')
        return dict(self.cursor.fetchall())

    def get_category_breakdown(self, trans_type="Expense"):
        """Get totals by category for a specific transaction type."""
        self.cursor.execute('''
            SELECT category, SUM(amount) 
            FROM transactions 
            WHERE type = ? 
            GROUP BY category
        ''', (trans_type,))
        return self.cursor.fetchall()

    def delete_transaction(self, trans_id):
        """Delete a transaction by ID."""
        self.cursor.execute('DELETE FROM transactions WHERE id = ?', (trans_id,))
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
