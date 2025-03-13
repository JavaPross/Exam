import sqlite3, datetime

conn = sqlite3.connect("library.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, copies INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT UNIQUE)''')
c.execute('''CREATE TABLE IF NOT EXISTS borrowings (id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER, borrow_date TEXT, return_date TEXT, FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(book_id) REFERENCES books(id))''')
conn.commit()

def execute(query, params=()):
    c.execute(query, params)
    conn.commit()

def fetch(query, params=()):
    c.execute(query, params)
    return c.fetchall()

def add_book(title, author, year, copies): execute("INSERT INTO books VALUES (NULL, ?, ?, ?, ?)", (title, author, year, copies))

def register_user(fname, lname, email): execute("INSERT INTO users VALUES (NULL, ?, ?, ?)", (fname, lname, email))

def borrow_book(uid, bid):
    if fetch("SELECT copies FROM books WHERE id = ?", (bid,))[0][0] > 0:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        execute("INSERT INTO borrowings VALUES (NULL, ?, ?, ?, ?)", (uid, bid, date, date))
        execute("UPDATE books SET copies = copies - 1 WHERE id = ?", (bid,))

def return_book(bid):
    book_id = fetch("SELECT book_id FROM borrowings WHERE id = ?", (bid,))
    if book_id:
        execute("DELETE FROM borrowings WHERE id = ?", (bid,))
        execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (book_id[0][0],))

def available_books(): print(fetch("SELECT * FROM books WHERE copies > 0"))

def borrowing_history(): print(fetch("SELECT * FROM borrowings"))

if __name__ == "__main__":
    add_book("Война и мир", "Л. Толстой", 1869, 3)
    register_user("Иван", "Иванов", "ivan@example.com")
    borrow_book(1, 1)
    available_books()
    borrowing_history()
    return_book(1)
    available_books()
    borrowing_history()

conn.close()

