import sqlite3, datetime

conn = sqlite3.connect("library.db")
conn.executescript('''
CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, copies INTEGER);
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT UNIQUE);
CREATE TABLE IF NOT EXISTS borrowings (id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER, borrow_date TEXT, return_date TEXT, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(book_id) REFERENCES books(id));
''')

run = lambda q, p=(), f=False: (c := conn.execute(q, p)).fetchall() if f else conn.commit() or None
add_book = lambda t, a, y, c: run("INSERT INTO books (title, author, year, copies) VALUES (?, ?, ?, ?)", (t, a, y, c))
register_user = lambda f, l, e: run("INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)", (f, l, e))
available_books = lambda: run("SELECT * FROM books WHERE copies > 0", f=1)
borrowing_history = lambda: run("SELECT * FROM borrowings", f=1)

def borrow_book(uid, bid):
    if run("SELECT copies FROM books WHERE id = ?", (bid,), 1)[0][0] > 0:
        run("INSERT INTO borrowings (user_id, book_id, borrow_date) VALUES (?, ?, ?)", (uid, bid, datetime.datetime.now().strftime('%Y-%m-%d')))
        run("UPDATE books SET copies = copies - 1 WHERE id = ?", (bid,))

def return_book(bid):
    if (b := run("SELECT book_id FROM borrowings WHERE id = ?", (bid,), 1)):
        run("UPDATE borrowings SET return_date = ? WHERE id = ?", (datetime.datetime.now().strftime('%Y-%m-%d'), bid))
        run("UPDATE books SET copies = copies + 1 WHERE id = ?", (b[0][0],))

if __name__ == "__main__":
    add_book("Война и мир", "Л. Толстой", 1869, 3)
    register_user("Иван", "Иванов", "ivan@example.com")
    borrow_book(1, 1)
    print(available_books(), borrowing_history())
    return_book(1)
    print(available_books(), borrowing_history())
    conn.close()
