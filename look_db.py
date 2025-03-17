import sqlite3
import os

# Specify the database filename here
DB_FILENAME = "db/giacomo3.sqlite"

def analyze_database():
    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the database file
    db_path = os.path.join(current_dir, DB_FILENAME)

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"Database: {db_path}")
        print(f"Number of tables: {len(tables)}")
        print("\nTable Information:")

        # Iterate through each table
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")

            # Get schema for the current table
            cursor.execute(f"PRAGMA table_info('{table_name}')")
            columns = cursor.fetchall()

            print("Columns:")
            for column in columns:
                print(f"  - {column[1]} ({column[2]})")

            # Get the number of rows in the table
            cursor.execute(f"SELECT COUNT(*) FROM '{table_name}'")
            row_count = cursor.fetchone()[0]
            print(f"Number of rows: {row_count}")

        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    analyze_database()