import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    type TEXT,
    category TEXT,
    date TEXT,
    description TEXT,
    user_id INTEGER
)
""")

cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role, status) VALUES (1,'Kishore','kishore@gmail.com','pass123','admin','active')")
cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role, status) VALUES (2,'Jeeva','jeeva@gmail.com','pass456','analyst','active')")
cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role, status) VALUES (3,'Ravi','ravi@gmail.com','pass789','viewer','active')")

cursor.execute("""
INSERT OR IGNORE INTO records (id, amount, type, category, date, description, user_id)
VALUES 
(1,5000,'income','salary','2026-04-06','Monthly salary',1),
(2,200,'expense','food','2026-04-06','Lunch',2),
(3,150,'expense','transport','2026-04-06','Bus fare',2)
""")

conn.commit()
conn.close()

print("Database created and sample data added as finance.db")