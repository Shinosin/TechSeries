import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Execute the SQL command to create the foodItem table
cursor.execute('''
CREATE TABLE IF NOT EXISTS foodItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    foodItemName TEXT NOT NULL,
    expiryDate DATE
)
''')
print("Created foodItem table successfully!")

cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email varchar NOT NULL,
    password varchar NOT NULL
)
''')
print("Created user table successfully!")

cursor.execute('''
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    expiry_date TEXT NOT NULL
)          
''')
print("Created inventory table successfully!")

# Commit the changes
conn.commit()

# Close the connection
conn.close()