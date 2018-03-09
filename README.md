Please find below the comments for the Project Requirements:

1) Registration: Users should be able to register for your website, providing (at minimum) a username and password.
-- Yes, it works. Users are able to register.

2) Login: Users, once registered, should be able to log in to your website with their username and password.
-- Yes, it works. Users are able to login with their registered credentials.

3) Logout: Logged in users should be able to log out of the site.
-- Did not get a chance to plug this functionality.

4) Import: Books.csv
-- The Python program "import.py" takes care of this by (i) creating the tables if they dont exist, and (ii) import the books if they have not been done already.

5) Search: Once a user has logged in, they should be taken to a page where they can search for a book. Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!
-- Yes, it works. Users are able to search by either of ISBN, Title or Author.

6) Book Page: When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.
-- Yes, users can navigate through hyperlinks from book search results.

7) Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
-- Yes, users can submit (i) rating, and (ii) reviews. And, it can only be submitted once.

8) Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
-- Yes, Goodreads has been intergrated with the website to showcase (i) Average Rating, and (ii) Number of ratings, if available. If its not, it displays "zero".

9) API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.
-- Yes, it works. Usrs can use the API web-link to access details in JSON format.


Things I couldn't get a chance to complete:
1) Session management -- The website works fine for a logged in user, but without session control, it forgets about the user if an exception/error page is thrown, or when search results are complete. I couldn't get a chance to code this functionality. Apologies.

2) Look and Feel -- I have used the very basic format for this web-site. I had plans to plug in the css/bootsrapcdn to make it more presentable, but could not due get a chance. I focussed more on the core-structure given the lack of time with me this time. Apologies for that.

Please review this project. I will appreciate any feedback or suggestions.

Thanks,
Gaurav
