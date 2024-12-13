import sqlite3

def add_new_row(db_path, table_name, date, account_name, data):
    """
    Add a new row to the database with 0.0 as default for missing numerical data.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all column names from the table
        cursor.execute(f"PRAGMA table_info({table_name})")
        all_columns = [col[1] for col in cursor.fetchall()]
        
        # Check if row already exists
        cursor.execute(f"""
            SELECT COUNT(*) FROM {table_name} 
            WHERE date = ? AND account_name = ?
        """, (date, account_name))
        
        if cursor.fetchone()[0] > 0:
            print(f"\nRow already exists for date {date} and account {account_name}")
            return
            
        # Prepare data for new row with defaults
        new_row_data = {'date': date, 'account_name': account_name}
        
        # Add all columns with 0.0 as default for missing numerical data
        for column in all_columns:
            if column not in ['date', 'account_name']:
                new_row_data[column] = data.get(column, 0.0)
        
        # Create INSERT statement
        columns_str = ', '.join(new_row_data.keys())
        placeholders = ', '.join(['?' for _ in new_row_data])
        values = list(new_row_data.values())
        
        cursor.execute(f"""
            INSERT INTO {table_name} ({columns_str})
            VALUES ({placeholders})
        """, values)
        
        conn.commit()
        print("\nNew row created successfully!")
        
        # Show the new row
        cursor.execute(f"""
            SELECT * FROM {table_name} 
            WHERE date = ? AND account_name = ?
        """, (date, account_name))
        
        new_row = cursor.fetchone()
        
        print("\nNewly Created Row:")
        for col, val in zip(all_columns, new_row):
            print(f"{col}: {val}")
            
    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":

    # Example usage - modify these values as needed:
    db_path = "db/new-database.db"
    table_name = "daily_reports"
    date = "2024-12-09"
    account_name = "simonegrup"

    # Add/modify the values you want to insert
    new_data = {
        'equity': 1595.0,
        'deposit': 1595.0,
    }

    add_new_row(db_path, table_name, date, account_name, new_data)