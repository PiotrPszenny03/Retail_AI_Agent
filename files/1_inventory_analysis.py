import pandas as pd
import numpy as np

def generate_and_analyze_inventory():
    print("Generating simulated inventory data...")
    np.random.seed(42)  # For reproducible results

    # Create 100 products (e.g., clothing, shoes)
    n_products = 100
    categories = ['T-shirt', 'Pants', 'Jacket', 'Shoes', 'Accessories']

    data = {
        'product_id': [f"SKU-{1000+i}" for i in range(n_products)],
        'category': np.random.choice(categories, n_products),
        'unit_cost': np.random.uniform(20, 150, n_products).round(2),  # Production cost
        'stock_level': np.random.randint(10, 500, n_products),  # Units in stock
        'days_in_inventory': np.random.randint(5, 180, n_products),  # How long they've been stored
        'elasticity': np.random.uniform(-2.5, -0.5, n_products).round(2)  # Price elasticity (e.g., -2.0 means a 10% discount boosts sales by 20%)
    }

    df = pd.DataFrame(data)

    # Markup (e.g., 150% of cost) -> this gives us the regular price
    df['regular_price'] = (df['unit_cost'] * 2.5).round(2)

    # Business assumption: storage costs 0.05 PLN per day per unit
    storage_cost_per_day = 0.05

    print("Calculating costs and margins...")
    # Calculate total storage cost for one unit
    df['total_storage_cost'] = (df['days_in_inventory'] * storage_cost_per_day).round(2)

    # Current gross margin (Price - Production cost - Storage cost)
    df['current_margin_pln'] = (df['regular_price'] - df['unit_cost'] - df['total_storage_cost']).round(2)
    df['margin_percentage'] = ((df['current_margin_pln'] / df['regular_price']) * 100).round(1)

    # BUSINESS CRITERIA - looking for issues:
    # 1. Stored longer than 90 days
    # 2. OR margin dropped below 20% due to storage costs
    problem_mask = (df['days_in_inventory'] > 90) | (df['margin_percentage'] < 20.0)

    problematic_df = df[problem_mask].copy()

    print(f"\nScan complete. Found {len(problematic_df)} problematic products out of {n_products}.")

    # Display the 5 worst cases (sorted by lowest margin)
    worst_products = problematic_df.sort_values(by='margin_percentage').head(5)
    print("\nTop 5 'margin-burning' products:")
    print(worst_products[['product_id', 'category', 'days_in_inventory', 'margin_percentage', 'elasticity']])

    # Save the full inventory and selected problems to CSV
    df.to_csv('full_inventory.csv', index=False)
    problematic_df.to_csv('problematic_products.csv', index=False)
    print("\nData saved to: 'full_inventory.csv' and 'problematic_products.csv'")

if __name__ == "__main__":
    generate_and_analyze_inventory()