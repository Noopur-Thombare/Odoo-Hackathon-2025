import sqlite3

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
