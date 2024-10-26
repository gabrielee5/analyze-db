import sqlite3

conn = sqlite3.connect('db/gabriele.sqlite')
conn.execute('PRAGMA wal_checkpoint(FULL)')
conn.close()

print("Done.")