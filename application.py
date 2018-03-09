from flask import Flask, flash, redirect, render_template, request, session, abort, json, jsonify
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os, requests


app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Already logged in!"

# Login function:
@app.route('/login', methods=['POST','GET'])
def login():
    try:
        global username
        global password
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).rowcount == 1:
            return render_template("tbr.html")
        else:
            return render_template("fail.html", message="Invalid UserName or Password. Please try again.")
    except ValueError:
        return render_template("fail.html", message="Something went wrong. Please try again.")
    return username, password

# Register New Users:
@app.route("/registration")
def registration():
    if not session.get('logged_in'):
        return render_template('registration.html')
    else:
        return "Already logged in!"

# Add  new users:
@app.route("/adduser", methods=["POST"])
def adduser():
    try:
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))
        email = str(request.form.get("email"))
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
            db.execute("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)",
                        {"username": username, "password": password, "email": email})
            db.commit()
            return render_template("success.html")
        else:
            return render_template("exists.html", message="User already exists. Please login.")
    except ValueError:
        return render_template("error.html", message="Registration Failed. Please try again.")

# Search for books:
@app.route("/books", methods=["POST"])
def books():
    try:
        global isbn
        global title
        global author
        global year
        isbn = str(request.form.get("isbn"))
        title = str(request.form.get("title"))
        author = str(request.form.get("author"))

        results = db.execute("SELECT * FROM books WHERE isbn = :isbn OR title = :title OR author = :author",
                         {"isbn": isbn, "title": title, "author": author}).fetchall()

        return render_template("books.html", results=results)

    except ValueError:
        return render_template("tbr.html", message="Something went wrong. Please try again.")

    return isbn, title, author, year

# Book search results (inclues reviews from this website and Goodreads)
@app.route("/books/<int:book_isbn>", methods=["POST", "GET"])
def book(book_isbn):
    global book_isbns
    global books
    global reviews
    global avg_rating
    global gr_avg_rating
    global gr_avg_rating_count

    # Check if the book searched exists or not:
    book_isbns = str(book_isbn)
    book = db.execute("SELECT * FROM books where isbn = :isbn", {"isbn": book_isbns}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")

    avg_rate = db.execute("SELECT avg(rating) as avgrating FROM reviews where isbn = :isbn", {"isbn": book_isbns}).fetchone()
    avg_rating_temp = avg_rate[0]
    if avg_rating_temp is None:
        avg_rating = 0
    else:
        avg_rating = format(round(avg_rating_temp,2))

    # Fetch reviews if available:
    reviews = db.execute("SELECT * FROM reviews where isbn = :isbn", {"isbn": book_isbns}).fetchall()

    gr_avg_rating = 0
    gr_avg_rating_count = 0

    # Goodreads Key:
    goodreadskey = "njlxn51n9PAOhW5yqdTQ"

    # Goodreads query:
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": goodreadskey, "isbns": book_isbns})
    if goodreads.status_code != 200:
        return render_template("book.html", book=book, reviews=reviews, avg_rating=avg_rating, gr_avg_rating=gr_avg_rating, gr_avg_rating_count=gr_avg_rating_count)

    goodreadreviewtemp1 = goodreads.json()
    goodreadreviewtemp2 = goodreadreviewtemp1["books"]
    goodreadreviewtemp3 = goodreadreviewtemp2[0]

    gr_avg_rating = goodreadreviewtemp3["average_rating"]
    gr_avg_rating_count = goodreadreviewtemp3["ratings_count"]

    # Return results
    return render_template("book.html", book=book, reviews=reviews, avg_rating=avg_rating, gr_avg_rating=gr_avg_rating, gr_avg_rating_count=gr_avg_rating_count)

# Submit rating and review, and display the posted review immediately:
@app.route("/ratingreview", methods=["POST"])
def ratingreview():
    try:
        rating = str(request.form.get("rating"))
        review = str(request.form.get("review"))
        #username = login(username)
        if db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn AND title = :title AND author = :author",
                         {"username": username, "isbn": book_isbns, "title": title, "author": author}).rowcount == 0:
            db.execute("INSERT INTO reviews (isbn, title, author, rating, review, username) VALUES (:isbn, :title, :author, :rating, :review, :username)",
                        {"isbn": book_isbns, "title": title, "author": author, "rating": rating, "review": review, "username": username})

            db.commit()

            reviews = db.execute("SELECT * FROM reviews where isbn = :isbn", {"isbn": book_isbns}).fetchall()

            return render_template("book.html", book=book, reviews=reviews, avg_rating=avg_rating, gr_avg_rating=gr_avg_rating, gr_avg_rating_count=gr_avg_rating_count)

        else:
            return render_template("exists.html", message="You have already submitted a rating/review for this book.")
    except ValueError:
        return render_template("error.html", message="Review submission failed. Please try again.")


# API function:
@app.route("/api/isbn/<string:isbn>")
def isbn_api(isbn):
    """Return details about a single isbn."""

    isbnresult = db.execute("SELECT books.isbn, books.title, books.author, books.year, COUNT(reviews.review) AS review_count, to_char( float8 (avg(reviews.rating)) , 'FM999999999.00' ) AS average_score FROM books LEFT JOIN reviews ON books.isbn = reviews.isbn  WHERE books.isbn = :isbn group by books.isbn, books.title, books.author, books.year, reviews.review, reviews.rating", {"isbn": isbn}).fetchone()

    if isbnresult is None:
        return jsonify({"error": "Invalid isbn"}), 422

    return jsonify({
            "title": isbnresult.title,
            "author": isbnresult.author,
            "year": isbnresult.year,
            "isbn": isbnresult.isbn,
            "review_count": isbnresult.review_count,
            "average_score": isbnresult.average_score
        })
