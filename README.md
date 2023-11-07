# Selvä vastaus
"Selvä vastaus", which means "Clear answer", is a service for individuals interested in studying the Finnish language. Here, you can discover Finnish words that are often difficult to find elsewhere. I created it for my own purposes because I am simultaneously studying Finnish and IT. This website is my final project for the "CS50's Introduction to Computer Science" free course at Harvard University. When I study Finnish grammar, I need to know word endings every time. Understanding how Finnish words can flex in different cases is crucial. I am open to your suggestions and recommendations to improve the website. You can contact me by email at romashkoyp(a)gmail.com
### Video Demo:  <https://youtu.be/EX3DdnMBRFY>
### Description, app.py
This documentation covers the Flask web application designed for managing a database of words. It provides an interface for users to interact with the `words.db` SQLite database and perform various operations based on Finnish linguistic features.
### Requirements
- Python 3.x
- Flask
- CS50 Library
- re (Regular Expression module)
### Code Structure
### Import Statements
The application requires several modules to function properly. These are imported at the beginning of the script:
- import re - is used for regular expressions, allowing us to validate user input
- from cs50 import SQL - is used to interact with the SQLite database
- from flask import Flask, render_template, request, session - are used to create and manage the web application
### Regular Expression Whitelist
The following regular expression is used to validate user inputs to ensure they only contain permissible characters, including Finnish letters and commas:
```
whitelist_pattern = r'^[a-zA-ZäÄöÖåÅ,]+$'
```
### The valid_input Function
This function takes an input string and checks it against the whitelist pattern to ensure it is valid:
```
def valid_input(input_string):
    return re.match(whitelist_pattern, input_string) is not None
```
### Flask Application Configuration
The Flask app is configured with a secret key, which is essential for securely managing sessions:
```
app = Flask(__name__)
app.secret_key = '4hH+C4g*7YAv'
```
### Database Configuration
The CS50 library is used to set up an interface with the SQLite database:
```
db = SQL("sqlite:///words.db")
```
### Routes and View Functions
The application has several routes that correspond to different pages and functionalities:
### Index Route
 The index route ("/") handles the main page and its interactions:
```
@app.route("/", methods=["GET", "POST"])
```
Depending on whether the request method is GET or POST, it will display the search form or process the submitted data, respectively.
### About Route
Provides information about the application and its purpose:
```
@app.route("/about")
```
### SQL Query Construction
The application dynamically constructs SQL queries based on user input, utilizing placeholders and conditions to retrieve the correct data from the database. Each query consists of two parts: the first calculates the number of words in the query, and the second executes the main query with the actual data.
## words.db
This database includes 6 tables of content for querying. The 'words' column in each table is indexed for improved search speed, as the database contains more than 500,000 rows.
## create_db.py and fill_db.py
Scripts for creating and filling the database from 6 different CSV files located in the 'Source' folder are provided, useful for refreshing the database with new data.
## layout.html
A template with Jinja that incorporates Bootstrap links and contains HTML for the header and footer.
## index.html
A template that displays three variants of the webpage:
- With a GET request method, it shows the basic webpage with input forms and a description of the website.
- With a POST request method and correct user input, it displays the search results.
- With a POST request method and zero results, it shows a 'no result' template.
## error.html
Displayed when a user inputs incorrect characters in the input fields.
## about.html
Displayed when the 'About' link in the footer is clicked, providing more technical information and sources.
## static
A folder containing files for the favicon, logo, special font for the website, CSS styles, and a JavaScript file.
