import sqlite3
import os

db_path = 'instance/todo.db'
print(f"Connecting to database at: {os.path.abspath(db_path)}")

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Check schema
print("Current columns in 'todo' table:")
c.execute("PRAGMA table_info(todo)")
columns = [row[1] for row in c.fetchall()]
print(columns)

if 'due_date' not in columns:
    print("Adding due_date column...")
    try:
        c.execute('ALTER TABLE todo ADD COLUMN due_date DATETIME')
        print("Success.")
    except Exception as e:
        print(f"Error adding due_date: {e}")

if 'priority' not in columns:
    print("Adding priority column...")
    try:
        c.execute('ALTER TABLE todo ADD COLUMN priority VARCHAR(10) DEFAULT "Medium"')
        print("Success.")
    except Exception as e:
        print(f"Error adding priority: {e}")

if 'date_completed' not in columns:
    print("Adding date_completed column...")
    try:
        c.execute('ALTER TABLE todo ADD COLUMN date_completed DATETIME')
        print("Success.")
    except Exception as e:
        print(f"Error adding date_completed: {e}")

conn.commit()
conn.close()
