import sqlite3

def view_and_modify_row(db_path, table_name, date, account_name, updates):
    """
    View and modify a row based on date and account_name.
    
    Args:
        db_path: Path to SQLite database
        table_name: Name of the table
        date: Date in YYYY-MM-DD format
        account_name: Name of the account
        updates: Dictionary of {column_name: new_value} to update
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Show the row before update
        cursor.execute(f"""
            SELECT * FROM {table_name} 
            WHERE date = ? AND account_name = ?
        """, (date, account_name))
        
        before_row = cursor.fetchone()
        
        if not before_row:
            print(f"No row found for date {date} and account {account_name}")
            return
            
        print("\nBefore Update:")
        for col, val in zip(columns, before_row):
            print(f"{col}: {val}")
            
        # Perform the update
        set_clause = ', '.join([f"{col} = ?" for col in updates.keys()])
        values = list(updates.values())
        values.extend([date, account_name])  # Add WHERE conditions
        
        cursor.execute(f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE date = ? AND account_name = ?
        """, values)
        
        # Show the row after update
        cursor.execute(f"""
            SELECT * FROM {table_name} 
            WHERE date = ? AND account_name = ?
        """, (date, account_name))
        
        after_row = cursor.fetchone()
        
        print("\nAfter Update:")
        for col, val in zip(columns, after_row):
            print(f"{col}: {val}")
        
        conn.commit()
        print("\nUpdate successful!")
        
    except sqlite3.Error as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":

    db_path = "db/database2.db"
    table_name = "daily_reports"
    date = "2025-01-02"
    account_name = "manuelp"

    # Updates to make
    updates = {
        'equity': 1210.0,
        # add other columns you want to update
    }

    view_and_modify_row(db_path, table_name, date, account_name, updates)