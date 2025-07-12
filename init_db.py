import sqlite3

<<<<<<< HEAD
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
=======
# Connect to database (or create if it doesn't exist)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table for profiles
c.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        skills_offered TEXT,
        skills_needed TEXT,
        availability TEXT
    )
''')

# Save and close
conn.commit()
conn.close()

print("✅ profiles table created!")
>>>>>>> d287679bf1a62fa0d2e674c94f65881bba75e939
