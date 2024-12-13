import os
import sqlite3
import csv
from datetime import datetime
import pandas as pd

# Function to generate filename with versioning
def get_filename(base_name, extension, csv_folder):
    # Get current date for filename
    current_date = datetime.now().strftime("%Y-%m-%d")
    version = 1
    while True:
        if version == 1:
            filename = f"{base_name}_{current_date}.{extension}"
        else:
            filename = f"{base_name}_{current_date}_v{version}.{extension}"
        if not os.path.exists(os.path.join(csv_folder, filename)):
            return filename
        version += 1

def convert_sqlite_to_csv(from_path):
    # Set the current directory and paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, from_path)
    
    # Create 'data_csv' folder if it doesn't exist
    csv_folder = os.path.join(current_dir, 'data_csv')
    os.makedirs(csv_folder, exist_ok=True)
    
    csv_filename = get_filename("output", "csv", csv_folder)
    csv_path = os.path.join(csv_folder, csv_filename)

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute a SELECT query to fetch all data from the table
        cursor.execute("""
            SELECT * FROM daily_reports 
            ORDER BY date ASC
        """)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Write data to CSV file
        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # Write header
            csv_writer.writerow(column_names)
            
            # Write data rows
            csv_writer.writerows(rows)

        print(f"Data successfully exported to {csv_path}")
        return csv_path

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

def convert_csv_to_excel(from_path):
    # Read the CSV file
    df = pd.read_csv(from_path)

    current_dir = os.path.dirname(os.path.abspath(__file__))

    xlsx_folder = os.path.join(current_dir, 'data_xlsx')
    os.makedirs(xlsx_folder, exist_ok=True)

    file_name = get_filename('output', 'xlsx', xlsx_folder)
    xlsx_path = os.path.join(xlsx_folder, file_name)
    
    # Write to XLSX file
    df.to_excel(xlsx_path, index=False)
    
    print(f"Excel file created: {xlsx_path}")
    return xlsx_path

if __name__ == "__main__":
    from_path = 'db/database-copy.db'
    csv_path = convert_sqlite_to_csv(from_path)
    # xlsx_path = convert_csv_to_excel(csv_path)
    print(f"Process completed.")