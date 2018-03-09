import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # Create Database Table(s) if not exist:

    # Table "users"
    db.execute("""CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        email VARCHAR NOT NULL)"""
        )


    # Table "books"
    db.execute("""CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        isbn VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL,
        year INTEGER NOT NULL)"""
        )

    # Table "reviews"
    db.execute("""CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER,
    rating INTEGER,
    review VARCHAR,
    username VARCHAR)"""
        )
    db.commit()


    # Import books.csv into table "books" created above.
    # Before "import", the program checks if the rows have already been imported or not. If "not", only then it will "import".

    status = db.execute("""SELECT COUNT(*) FROM books""").fetchone()
    rowcount = status[0]
    if rowcount >= 5000:
        print (f"Already {rowcount} rows imported into DB. Not importing anymore.")
    else:
        print (f"No rows availabe in DB at the moment. Importing rows now.")

        f = open("books.csv")
        reader = csv.reader(f)
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added books with ISBN as {isbn}, Title as {title}, Author as {author} and Year as {year}.")
            db.commit()

if __name__ == "__main__":
    main()
