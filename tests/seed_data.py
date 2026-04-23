from src.core.finance_manager import FinanceManager
from datetime import datetime, timedelta
import random

def seed_database():
    manager = FinanceManager()
    
    categories = {
        "Income": ["Salary", "Freelance", "Investment", "Bonus"],
        "Expense": ["Rent", "Groceries", "Dining", "Utilities", "Transport", "Entertainment", "Shopping"]
    }
    
    descriptions = {
        "Salary": ["Monthly Salary", "Project Bonus"],
        "Freelance": ["Web Design Client", "Logo Design"],
        "Rent": ["Apartment Rent", "Office Space"],
        "Groceries": ["Walmart", "Whole Foods", "Local Market"],
        "Dining": ["Starbucks", "Pizza Hut", "Fine Dining"],
        "Utilities": ["Electricity Bill", "Water Bill", "Internet"],
        "Transport": ["Uber Ride", "Gas Station", "Bus Pass"],
        "Entertainment": ["Netflix Subscription", "Movie Tickets", "Gym Membership"],
        "Shopping": ["Amazon Purchase", "Clothing", "Electronics"]
    }

    # Start from 30 days ago
    start_date = datetime.now() - timedelta(days=30)
    
    print("Seeding database with random transactions...")

    for i in range(25):
        t_type = random.choice(["Income", "Expense", "Expense", "Expense"]) # More expenses than income
        category = random.choice(categories[t_type])
        desc = random.choice(descriptions.get(category, ["Miscellaneous"]))
        amount = round(random.uniform(100, 5000), 2) if t_type == "Expense" else round(random.uniform(10000, 50000), 2)
        
        # Random date within the last 30 days
        t_date = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        date_str = t_date.strftime("%d %b %Y, %H:%M")
        
        manager.add_entry(date_str, desc, category, t_type, amount)

    print("Success! 25 transactions added.")
    manager.close()

if __name__ == "__main__":
    seed_database()
