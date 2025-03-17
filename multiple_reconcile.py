import os
import sqlite3

def checkpoint_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute('PRAGMA wal_checkpoint(FULL)')
        conn.close()
        print(f"Successfully checkpointed: {db_path}")
        return True
    except sqlite3.Error as e:
        print(f"Error processing {db_path}: {e}")
        return False

def process_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    # Walk through all files in the folder and subfolders
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Check if file has a .sqlite or .db extension
            if file.endswith(('.sqlite', '.db')):
                db_path = os.path.join(root, file)
                if checkpoint_database(db_path):
                    success_count += 1
                else:
                    error_count += 1
            else:
                skipped_count += 1
    
    print("\nCheckpoint Summary:")
    print(f"Processed successfully: {success_count}")
    print(f"Errors encountered: {error_count}")
    print(f"Non-database files skipped: {skipped_count}")

if __name__ == "__main__":
    # You can change the folder path here
    db_folder = "db/every_db/db"
    
    print(f"Starting WAL checkpoint process on folder: {db_folder}")
    process_folder(db_folder)
    print("Done.")