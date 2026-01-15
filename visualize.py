import matplotlib.pyplot as plt
from database import get_monthly_summary, get_category_summary
import os

def create_visualizations():
    """Generate and save financial visualizations."""
    
    # Create output directory if it doesn't exist
    if not os.path.exists('charts'):
        os.makedirs('charts')
    
    print("Generating visualizations...\n")
    
    # 1. Monthly Income vs Expenses
    monthly_df = get_monthly_summary()
    
    if not monthly_df.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(monthly_df))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], monthly_df['income'], 
               width, label='Income', color='green', alpha=0.7)
        ax.bar([i + width/2 for i in x], monthly_df['expenses'], 
               width, label='Expenses', color='red', alpha=0.7)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Monthly Income vs Expenses')
        ax.set_xticks(x)
        ax.set_xticklabels(monthly_df['month'], rotation=45)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('charts/monthly_summary.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: charts/monthly_summary.png")
        plt.close()
    
    # 2. Category Breakdown Pie Chart
    category_df = get_category_summary()
    
    if not category_df.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Only show top 8 categories, group rest as "Other"
        if len(category_df) > 8:
            top_categories = category_df.head(8)
            other_amount = category_df.tail(len(category_df) - 8)['total_amount'].sum()
            
            categories = list(top_categories['category']) + ['Other']
            amounts = list(top_categories['total_amount']) + [other_amount]
        else:
            categories = category_df['category']
            amounts = category_df['total_amount']
        
        colors = plt.cm.Set3(range(len(categories)))
        
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
               startangle=90, colors=colors)
        ax.set_title('Spending by Category')
        
        plt.tight_layout()
        plt.savefig('charts/category_breakdown.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: charts/category_breakdown.png")
        plt.close()
    
    # 3. Net Savings Trend
    if not monthly_df.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(monthly_df['month'], monthly_df['net'], 
                marker='o', linewidth=2, markersize=8, color='blue')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.fill_between(range(len(monthly_df)), monthly_df['net'], 0, 
                        where=(monthly_df['net'] > 0), color='green', alpha=0.2)
        ax.fill_between(range(len(monthly_df)), monthly_df['net'], 0, 
                        where=(monthly_df['net'] <= 0), color='red', alpha=0.2)
        
        ax.set_xlabel('Month')
        ax.set_ylabel('Net Savings ($)')
        ax.set_title('Monthly Net Savings Trend')
        ax.set_xticks(range(len(monthly_df)))
        ax.set_xticklabels(monthly_df['month'], rotation=45)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('charts/savings_trend.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: charts/savings_trend.png")
        plt.close()
    
    print("\n✓ All visualizations generated successfully!")
    print("  Check the 'charts' folder to view them.")

if __name__ == "__main__":
    create_visualizations()