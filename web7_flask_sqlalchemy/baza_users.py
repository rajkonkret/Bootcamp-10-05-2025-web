import sqlite3

try:
    conn = sqlite3.connect("data/cantor1.db")
    c = conn.cursor()

    # query = """
    # CREATE TABLE IF NOT EXISTS transactions (
    # id INTEGER PRIMARY KEY,
    # currency TEXT,
    # amount INTEGER,
    # user TEXT);
    # """
    #
    # c.execute(query)
    # conn.commit()

    create_users = """CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 0,
    is_admin BOOLEAN NOT NULL DEFAULT 0);
    """
    c.execute(create_users)
    conn.commit()

except sqlite3.Error as e:
    print("Błąd:", e)
finally:
    if conn:
        conn.close()
