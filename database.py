import sqlite3
import pandas as pd

def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect('finance.db')

def execute_query(query, params=None):
    """Execute a query and return results as a pandas DataFrame."""
    conn = get_connection()
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def insert_transaction(date, amount, category, description):
    """Insert a single transaction into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transactions (date, amount, category, description)
        VALUES (?, ?, ?, ?)
    ''', (date, amount, category, description))
    
    conn.commit()
    conn.close()

def get_all_transactions():
    """Retrieve all transactions."""
    query = '''
        SELECT 
            transaction_id,
            date,
            amount,
            category,
            description
        FROM transactions
        ORDER BY date DESC
    '''
    return execute_query(query)

def get_monthly_summary():
    """Get spending summary by month."""
    query = '''
        SELECT 
            strftime('%Y-%m', date) as month,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as expenses,
            SUM(amount) as net
        FROM transactions
        GROUP BY month
        ORDER BY month DESC
    '''
    return execute_query(query)

def get_category_summary():
    """Get spending summary by category."""
    query = '''
        SELECT 
            category,
            COUNT(*) as transaction_count,
            SUM(ABS(amount)) as total_amount,
            AVG(ABS(amount)) as avg_amount
        FROM transactions
        WHERE amount < 0
        GROUP BY category
        ORDER BY total_amount DESC
    '''
    return execute_query(query)

def get_top_expenses(limit=10):
    """Get the top N largest expenses."""
    query = '''
        SELECT 
            date,
            category,
            description,
            ABS(amount) as amount
        FROM transactions
        WHERE amount < 0
        ORDER BY amount DESC
        LIMIT ?
    '''
    return execute_query(query, params=(limit,))