import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from tabulate import tabulate

# freqtrade database

# Database filename
DB_FILENAME = "db/oliviero.sqlite"

def load_trades_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, DB_FILENAME)
    
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM trades"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Convert date strings to datetime objects
    df['open_date'] = pd.to_datetime(df['open_date'])
    df['close_date'] = pd.to_datetime(df['close_date'])
    
    return df

def load_orders_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, DB_FILENAME)
    
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM orders"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # # Convert date strings to datetime objects
    # df['open_date'] = pd.to_datetime(df['open_date'])
    # df['close_date'] = pd.to_datetime(df['close_date'])
    
    return df

def visualize_trades(df):
    plt.figure(figsize=(15, 10))
    plt.subplot(2, 2, 1)
    plt.title('Profit/Loss Distribution')
    df['realized_profit'].hist(bins=30)
    plt.xlabel('Realized Profit')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 2)
    plt.title('Trade Duration')
    df['duration'] = (df['close_date'] - df['open_date']).dt.total_seconds() / 3600  # in hours
    df['duration'].hist(bins=30)
    plt.xlabel('Duration (hours)')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 3)
    plt.title('Cumulative Profit Over Time')
    df_sorted = df.sort_values('close_date')
    plt.plot(df_sorted['close_date'], df_sorted['realized_profit'].cumsum())
    plt.xlabel('Date')
    plt.ylabel('Cumulative Profit')

    plt.subplot(2, 2, 4)
    plt.title('Profit by Pair')
    df.groupby('pair')['realized_profit'].sum().sort_values().plot(kind='bar')
    plt.xlabel('Pair')
    plt.ylabel('Total Profit')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

def print_trades_table(df):
    # Select a subset of columns to display
    columns_to_display = [
        'id', 'pair', 'is_open', 'open_date', 'close_date', 
        'open_rate', 'close_rate', 'amount', 'realized_profit', 
        'exit_reason', 'strategy'
    ]
    
    # Ensure all selected columns are in the dataframe
    columns_to_display = [col for col in columns_to_display if col in df.columns]
    
    # Display the table
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', None)  # Auto-detect terminal width
    pd.set_option('display.max_rows', None)  # Show all rows
    
    print("\nTrades Table:")
    print(df[columns_to_display].to_string(index=False))

def display_orders(df, limit=None):
    """
    Display orders in a nicely formatted table
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing orders data
    limit (int, optional): Number of rows to display. If None, displays all rows
    
    Returns:
    str: Formatted table as string
    """
    # Select the most relevant columns for display
    columns_to_show = [
        'id', 'ft_pair', 'side', 'order_type', 'status',
        'amount', 'filled', 'price', 'cost',
        'order_date', 'ft_is_open'
    ]
    
    # Create a copy of the dataframe with selected columns
    display_df = df[columns_to_show].copy()
    
    # Limit rows if specified
    if limit:
        display_df = display_df.head(limit)
    
    # Format numeric columns
    if 'price' in display_df.columns:
        display_df['price'] = display_df['price'].round(2)
    if 'cost' in display_df.columns:
        display_df['cost'] = display_df['cost'].round(2)
    if 'amount' in display_df.columns:
        display_df['amount'] = display_df['amount'].round(4)
    if 'filled' in display_df.columns:
        display_df['filled'] = display_df['filled'].round(4)
    
    # Create the table
    table = tabulate(
        display_df,
        headers='keys',
        tablefmt='psql',
        showindex=False,
        floatfmt='.4f'
    )
    
    print(table)

def main():
    df = load_trades_data()
    print_trades_table(df)
    visualize_trades(df)

    # df2 = load_orders_data()
    # display_orders(df2)




if __name__ == "__main__":
    main()