from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///game.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # user is trying to register
        username = request.form.get("username")
        password = request.form.get("password")
        passwordConfirm = request.form.get("confirmation")
        if username == "":
            return apology("Username missing")
        usernameCheck = db.execute(
            "SELECT * FROM users WHERE username = ?", username)

        # username not available
        if usernameCheck:
            return apology("User already exists")

        # missing password
        if password == "":
            return apology("Missing password")

        # passwords do not match
        if password != passwordConfirm:
            return apology("Passwords do not match")

        # register
        passwordHashed = generate_password_hash(password)
        # print(passwordHashed)
        loggedInId = db.execute(
            "INSERT INTO users (username, hash) VALUES(?,?)", username, passwordHashed)
        # print(loggedInId)
        session["user_id"] = loggedInId
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    wordList = db.execute(
        "SELECT * FROM words WHERE answer1 = ? OR answer2 = ? OR answer3 = ? ORDER BY RANDOM() LIMIT 1", 0, 0, 0)
    # wordList = db.execute("SELECT * FROM words WHERE answer1 = ? ORDER BY RANDOM() LIMIT 1", 1)
    if not wordList:
        return redirect("/progress")
    word = wordList[0]
    if request.method == "GET":

        print("inside get:", word)
        return render_template("index.html", word=word)

    else:
        print("inside post:", word)
        result = request.form.get("result")
        wordId = request.form.get("word_id")

        # get the answer 2 and move it to answer 3
        answer2 = db.execute(
            "SELECT * FROM words WHERE word_id = ?", wordId)[0]['answer2']
        db.execute("UPDATE words SET answer3 = ? WHERE word_id = ?",
                   answer2, wordId)

        # get the answer 1 and move it to answer 2
        answer1 = db.execute(
            "SELECT * FROM words WHERE word_id = ?", wordId)[0]['answer1']
        db.execute("UPDATE words SET answer2 = ? WHERE word_id = ?",
                   answer1, wordId)

        # overwrite answer 1 with new answer
        db.execute("UPDATE words SET answer1 = ? WHERE word_id = ?",
                   int(result), wordId)

        print("this is result", result)
        return redirect("/")


@app.route("/reset", methods=["POST"])
@login_required
def reset():
    print("reset triggered")
    db.execute("UPDATE words SET answer1 = ?, answer2 = ?", 0, 0)
    return redirect("/progress")


@app.route("/progress")
@login_required
def progress():
    words = db.execute("SELECT * FROM words")
    # print(words)
    return render_template("/progress.html", words=words)
