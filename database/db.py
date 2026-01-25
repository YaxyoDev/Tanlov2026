import sqlite3

DB_NAME = "users.db"

def init():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
                    id INTEGER,
                    full_name TEXT
                    );
    """)
    conn.commit()
    conn.close()

def add_admin(tg_id, name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO admins (id, full_name) VALUES (?, ?);
        """, (tg_id, name,))
    conn.commit()
    conn.close()



def check_admin(tg_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM admins WHERE tg_id = ?;
        """, (tg_id,))
    data = cur.fetchone()
    conn.close()
    return data

def get_admins_id():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM admins;
        """)
    data = cur.fetchall()
    conn.close()
    return data

def delete_admin(id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM admins WHERE id = ?;
        """, (id,))
    conn.commit()
    conn.close()