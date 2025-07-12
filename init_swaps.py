import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS swaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        requester_name TEXT,
        receiver_name TEXT,
        status TEXT
    )
''')

conn.commit()
conn.close()
print("✅ swaps table created!")
