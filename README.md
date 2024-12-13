# DB ANALYZER

Visualize structure of a db with look_db.

With reconcile_db the -shm and -val are integrated in the main .sqlite db.
Visualizer is specific for my db (freqtrade).

## Manage DB

The db file should be in the main directory.
Instructions for various options:

python3 manage_db.py --db database_name.db --list-tables

python3 manage_db.py --db database_name.db --table your_table --list-columns

python3 manage_db.py --db database_name.db --table your_table --column column_to_delete
