from database import (
    get_all_transactions,
    get_monthly_summary,
    get_category_summary,
    get_top_expenses
)

def print_separator():
    """Print a visual separator."""
    print("\n" + "="*60 + "\n")

def analyze_finances():
    """Run complete financial analysis and display results."""
    
    print("PERSONAL FINANCE ANALYSIS")
    print_separator()
    
    # 1. Monthly Summary
    print("📊 MONTHLY SUMMARY")
    print("-" * 60)
    monthly_df = get_monthly_summary()
    if not monthly_df.empty:
        print(monthly_df.to_string(index=False))
    else:
        print("No transactions found.")
    
    print_separator()
    
    # 2. Category Breakdown
    print("🏷️  SPENDING BY CATEGORY")
    print("-" * 60)
    category_df = get_category_summary()
    if not category_df.empty:
        print(category_df.to_string(index=False))
        
        # Calculate and show percentages
        total_expenses = category_df['total_amount'].sum()
        print(f"\nTotal Expenses: ${total_expenses:,.2f}")
    else:
        print("No expense transactions found.")
    
    print_separator()
    
    # 3. Top 10 Largest Expenses
    print("💰 TOP 10 LARGEST EXPENSES")
    print("-" * 60)
    top_expenses_df = get_top_expenses(10)
    if not top_expenses_df.empty:
        print(top_expenses_df.to_string(index=False))
    else:
        print("No expenses found.")
    
    print_separator()
    
    # 4. Overall Statistics
    print("📈 OVERALL STATISTICS")
    print("-" * 60)
    all_transactions = get_all_transactions()
    
    if not all_transactions.empty:
        total_income = all_transactions[all_transactions['amount'] > 0]['amount'].sum()
        total_expenses = abs(all_transactions[all_transactions['amount'] < 0]['amount'].sum())
        net_savings = total_income - total_expenses
        
        print(f"Total Income:     ${total_income:,.2f}")
        print(f"Total Expenses:   ${total_expenses:,.2f}")
        print(f"Net Savings:      ${net_savings:,.2f}")
        print(f"Savings Rate:     {(net_savings/total_income*100):.1f}%")
        print(f"Total Transactions: {len(all_transactions)}")
    else:
        print("No transactions to analyze.")
    
    print_separator()

if __name__ == "__main__":
    analyze_finances()