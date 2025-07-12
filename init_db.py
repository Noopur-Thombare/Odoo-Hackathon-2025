import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    skills_offered TEXT,
    skills_needed TEXT,
    availability TEXT,
    name TEXT  -- Optional: only if you're using {{ user['name'] }}
)
''')

# Create swaps table
cursor.execute('''
CREATE TABLE IF NOT EXISTS swaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id INTEGER,
    receiver_id INTEGER,
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (requester_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()
print("✅ Database, users table, and swaps table created.")
