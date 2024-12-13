import sqlite3
import argparse
import sys

def get_table_info(cursor, table_name):
    """Get information about table columns"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()

def delete_column(db_path, table_name, column_name):
    """Delete a column from a specified table"""
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get current table info
        columns = get_table_info(cursor, table_name)
        if not columns:
            print(f"Table '{table_name}' not found.")
            return False
            
        # Get all column names except the one to delete
        columns_to_keep = [col[1] for col in columns if col[1] != column_name]
        
        if len(columns_to_keep) == len(columns):
            print(f"Column '{column_name}' not found in table '{table_name}'.")
            return False
            
        # Create new table without the specified column
        columns_str = ', '.join(columns_to_keep)
        cursor.execute(f"""
            CREATE TABLE temp_table AS 
            SELECT {columns_str}
            FROM {table_name}
        """)
        
        # Drop old table
        cursor.execute(f"DROP TABLE {table_name}")
        
        # Rename temp table to original name
        cursor.execute(f"ALTER TABLE temp_table RENAME TO {table_name}")
        
        # Commit changes
        conn.commit()
        print(f"Successfully deleted column '{column_name}' from table '{table_name}'.")
        return True
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def list_tables(db_path):
    """List all tables in the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    finally:
        conn.close()

def list_columns(db_path, table_name):
    """List all columns in a table"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        columns = get_table_info(cursor, table_name)
        return [col[1] for col in columns]
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description='Delete a column from a SQLite database')
    parser.add_argument('--db', required=True, help='Path to the SQLite database')
    parser.add_argument('--table', help='Table name')
    parser.add_argument('--column', help='Column to delete')
    parser.add_argument('--list-tables', action='store_true', help='List all tables in the database')
    parser.add_argument('--list-columns', action='store_true', help='List all columns in the specified table')
    
    args = parser.parse_args()
    
    if args.list_tables:
        tables = list_tables(args.db)
        print("\nAvailable tables:")
        for table in tables:
            print(f"- {table}")
        return
        
    if args.list_columns and args.table:
        columns = list_columns(args.db, args.table)
        print(f"\nColumns in table '{args.table}':")
        for column in columns:
            print(f"- {column}")
        return
        
    if not args.table or not args.column:
        parser.print_help()
        return
        
    delete_column(args.db, args.table, args.column)

if __name__ == "__main__":
    main()