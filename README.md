# Aura Finance - Personal Tracker

Aura Finance is a modern, high-performance desktop application built with Python and Tkinter to help you track your income and expenses with ease.

## Features
- **Dashboard Summary**: Real-time tracking of Balance, Income, and Expenses.
- **Visual Analytics**: Interactive donut charts for category-wise expense analysis.
- **Persistent Data**: Powered by SQLite for reliable data storage.
- **Premium UI**: Clean, responsive-like interface with custom styling.
- **Currency Support**: Fully supports Indian Rupees (₹).

## Project Structure
```text
AuraFinance/
├── data/               # SQLite database storage
├── src/
│   ├── core/           # Database and business logic
│   └── ui/             # Tkinter GUI components
├── tests/              # Test scripts and data seeding
├── main.py             # Application entry point
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.x
- Matplotlib (`pip install matplotlib`)
- ttkbootstrap (Optional, for enhanced themes: `pip install ttkbootstrap`)

### Installation & Usage
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install matplotlib
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Development
To seed the database with sample data for testing, run:
```bash
python -m tests.seed_data
```

## License
MIT
