import sqlite3
import os

def create_database():
    """Initialize the SQLite database with required tables."""
    
    # Check if database already exists
    if os.path.exists('finance.db'):
        response = input("Database already exists. Overwrite? (yes/no): ")
        if response.lower() != 'yes':
            print("Setup cancelled.")
            return
        os.remove('finance.db')
    
    # Connect to database (creates it if doesn't exist)
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense'))
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            FOREIGN KEY (category) REFERENCES categories(name)
        )
    ''')
    
    # Insert default categories
    default_categories = [
        ('Income', 'income'),
        ('Salary', 'income'),
        ('Groceries', 'expense'),
        ('Rent', 'expense'),
        ('Utilities', 'expense'),
        ('Transportation', 'expense'),
        ('Entertainment', 'expense'),
        ('Healthcare', 'expense'),
        ('Shopping', 'expense'),
        ('Dining Out', 'expense'),
        ('Other', 'expense')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)',
        default_categories
    )
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("✓ Database created successfully!")
    print("✓ Default categories added")
    print("✓ Ready to import transactions")

if __name__ == "__main__":
    create_database()