import sqlite3


def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE)
    """)
    conn.commit()
    conn.close()


def get_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user


def add_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email) VALUES (?);", (email,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError: # bład gdy user już był w bazie danych
        conn.close()
        return False
