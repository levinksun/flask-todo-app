import sqlite3

def migrate():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    
    try:
        c.execute('ALTER TABLE todo ADD COLUMN due_date DATETIME')
        print("Added due_date column")
    except sqlite3.OperationalError:
        print("due_date column likely already exists")
        
    try:
        c.execute('ALTER TABLE todo ADD COLUMN priority VARCHAR(10) DEFAULT "Medium"')
        print("Added priority column")
    except sqlite3.OperationalError:
        print("priority column likely already exists")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
