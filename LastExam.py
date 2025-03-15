import sqlite3, datetime

conn = sqlite3.connect("library.db")
conn.executescript('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, copies INTEGER
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS borrowings (
    id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER, 
    borrow_date TEXT, return_date TEXT, 
    FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(book_id) REFERENCES books(id)
);
''')

def add_book(t, a, y, c): 
    conn.execute("INSERT INTO books (title, author, year, copies) VALUES (?, ?, ?, ?)", (t, a, y, c))
    conn.commit()

def register_user(f, l, e): 
    conn.execute("INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)", (f, l, e))
    conn.commit()

def borrow_book(uid, bid): 
    if conn.execute("SELECT copies FROM books WHERE id = ?", (bid,)).fetchone()[0] > 0:
        conn.execute("INSERT INTO borrowings (user_id, book_id, borrow_date) VALUES (?, ?, ?)", 
                     (uid, bid, datetime.datetime.now().strftime('%Y-%m-%d')))
        conn.execute("UPDATE books SET copies = copies - 1 WHERE id = ?", (bid,))
        conn.commit()

def return_book(bid): 
    book_id = conn.execute("SELECT book_id FROM borrowings WHERE id = ?", (bid,)).fetchone()
    if book_id:
        conn.execute("UPDATE borrowings SET return_date = ? WHERE id = ?", 
                     (datetime.datetime.now().strftime('%Y-%m-%d'), bid))
        conn.execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (book_id[0],))
        conn.commit()

add_book("Minecraft: The Official Guide", "Mojang Studios", 2021, 5)
register_user("Иван", "Иванов", "ivan@example.com")
borrow_book(1, 1)
print("Доступные книги:", conn.execute("SELECT * FROM books WHERE copies > 0").fetchall())
return_book(1)
print("История:", conn.execute("SELECT * FROM borrowings").fetchall())

conn.close()
