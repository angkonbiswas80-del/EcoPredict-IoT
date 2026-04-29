import sqlite3

conn = sqlite3.connect('cold_chain.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS shipment_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shipment_id TEXT,
        temperature REAL,
        humidity REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Database and Table created successfully!")