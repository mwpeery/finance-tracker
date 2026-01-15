import csv
import sqlite3
import sys
from datetime import datetime

def validate_date(date_string):
    """Validate and parse date string."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_amount(amount_string):
    """Validate amount is a valid number."""
    try:
        float(amount_string)
        return True
    except ValueError:
        return False

def import_csv(filename):
    """Import transactions from CSV file into database."""
    
    # Check if file exists
    try:
        with open(filename, 'r') as file:
            pass
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    
    # Connect to database
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    successful_imports = 0
    failed_imports = 0
    
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        # Validate headers
        required_headers = ['date', 'amount', 'category', 'description']
        if not all(header in csv_reader.fieldnames for header in required_headers):
            print(f"Error: CSV must have headers: {', '.join(required_headers)}")
            return
        
        for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (after header)
            # Validate date
            if not validate_date(row['date']):
                print(f"Row {row_num}: Invalid date format '{row['date']}' (use YYYY-MM-DD)")
                failed_imports += 1
                continue
            
            # Validate amount
            if not validate_amount(row['amount']):
                print(f"Row {row_num}: Invalid amount '{row['amount']}'")
                failed_imports += 1
                continue
            
            # Insert transaction
            try:
                cursor.execute('''
                    INSERT INTO transactions (date, amount, category, description)
                    VALUES (?, ?, ?, ?)
                ''', (row['date'], float(row['amount']), row['category'], row['description']))
                successful_imports += 1
            except sqlite3.Error as e:
                print(f"Row {row_num}: Database error - {e}")
                failed_imports += 1
    
    # Commit and close
    conn.commit()
    conn.close()
    
    # Print summary
    print(f"\n✓ Import complete!")
    print(f"  Successfully imported: {successful_imports} transactions")
    if failed_imports > 0:
        print(f"  Failed to import: {failed_imports} transactions")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_data.py <csv_filename>")
        print("Example: python import_data.py sample_transactions.csv")
    else:
        import_csv(sys.argv[1])