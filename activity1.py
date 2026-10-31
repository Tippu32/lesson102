import sqlite3
import pandas as pd

conn=sqlite3.connect(":memory:")

conn.execute("""CREATE TABLE author (author_id INTEGER PRIMARY KEY, author_name TEXT NOT NULL)""")

conn.execute("""CREATE TABLE book (book_id INTEGER PRIMARY KEY, book_title TEXT NOT NULL, author_id INTEGER
)""")

conn.executemany("INSERT INTO author VALUES (?, ?)", [(1, 'J.K. Rowling'), (2, 'George R.R. Martin'), (3, 'J.R.R. Tolkien'),(4, 'Agatha Christie'), (5, 'Stephen King'),(6, 'Dan Brown') ])

conn.executemany("INSERT INTO book VALUES (?, ?, ?)", [(1, 'Harry Potter and the Sorcerer\'s Stone', 1), (2, 'A Game of Thrones', 2), (3, 'The Hobbit', 3), (4, 'Murder on the Orient Express', 4), (5, 'The Shining', 5), (6, 'The Da Vinci Code', 6)])

conn.commit()

authors=pd.read_sql("SELECT * FROM author", conn)
books=pd.read_sql("SELECT * FROM book", conn)
print("Author Table:")
print(authors)
print()
print("Book Table:")
print(books)
print()

#part 2:inner join
inner=pd.read_sql(
    "SELECT author.author_name, book.book_title"
    "FROM author INNER JOIN book ON author.author_id = book.author_id",conn
)
print("Inner Join-authors matched with their books:")
print(inner)
print()

#part 3:LEFT JOIN
left = pd.read_sql(
    "SELECT author.author_name, book.book_title" "FROM author LEFT JOIN book ON author.author_id = book.author_id", conn
)
print("Left Join - All authors ,NULL where no book found:")
print(left)
print()

#part 4:CROSS JOIN
cross=pd.read_sql(
    "SELECT author.author_name, book.book_title FROM author CROSS JOIN book WHERE author.author_id <= 2", conn
)
print("Cross Join - first 2 authors paired with every book:")
print(cross)
print()

#part 5:UNION
union=pd.read_sql(
    "SELECT author_name AS name, 'Author' AS type FROM author UNION SELECT book_title AS name, 'Book' AS type FROM book", conn
)
print("Union - All author names and book titles combined:")
print(union)

conn.close()