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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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
        loggedInId = db.execute(
            "INSERT INTO users (username, hash) VALUES(?,?)", username, passwordHashed)
        session["user_id"] = loggedInId

        # create the empty answers for the new user
        words = db.execute("SELECT * FROM words")
        for word in words:
            db.execute(
                "INSERT INTO answers (user_id, word_id, answer1, answer2, answer3) VALUES(?,?,?,?,?)", session["user_id"], word['word_id'], 0, 0, 0)
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    currentUserId = session['user_id']
    print("this is the current user id: ", currentUserId)

    # get the word that is not answered correctly 3 times in a row
    wordList = db.execute(
        "SELECT * FROM words WHERE word_id NOT IN (SELECT word_id FROM answers WHERE user_id = ? AND answer1 = 1 AND answer2 = 1 AND answer3 = 1) ORDER BY RANDOM() LIMIT 1", currentUserId)

    # if all the words are answered correctly 3 times in a row, redirect to the progress route
    if not wordList:
        return redirect("/progress")

    word = wordList[0]
    if request.method == "GET":

        # get the streak info
        streak = db.execute("SELECT * FROM users WHERE user_id = ?", currentUserId)[0]['streak']
        
        # get total number of words
        totalWordCount = db.execute("SELECT COUNT(*) FROM answers WHERE user_id = ?", currentUserId)[0]['COUNT(*)']
        
        # get number of words user fully practiced (answered correctly 3 times in a row)
        fullyPracticedWordCount = db.execute("SELECT COUNT(*) FROM answers WHERE user_id = ? AND answer1 = 1 AND answer2 = 1 AND answer3 = 1", currentUserId)[0]['COUNT(*)']
        
        return render_template("index.html", word=word, streak=streak, totalWordCount=totalWordCount, fullyPracticedWordCount=fullyPracticedWordCount)

    else:
        result = request.form.get("result")
        wordId = request.form.get("word_id")

        # get the answer 2 and move it to answer 3
        answer2 = db.execute(
            "SELECT * FROM answers WHERE user_id = ? AND word_id = ?", currentUserId, wordId)[0]['answer2']
        db.execute("UPDATE answers SET answer3 = ? WHERE user_id = ? AND word_id = ?",
                   answer2, currentUserId, wordId)

        # get the answer 1 and move it to answer 2
        answer1 = db.execute(
            "SELECT * FROM answers WHERE user_id = ? AND word_id = ?", currentUserId, wordId)[0]['answer1']
        db.execute("UPDATE answers SET answer2 = ? WHERE user_id = ? AND word_id = ?",
                   answer1, currentUserId, wordId)

        # overwrite answer 1 with new answer
        db.execute("UPDATE answers SET answer1 = ? WHERE user_id = ? AND word_id = ?",
                   int(result), currentUserId, wordId)

        # if answered correctly, increase the streak by 1:
        if int(result) == 1:
            db.execute(
                "UPDATE users SET streak = streak + 1 WHERE user_id = ?", currentUserId)

        # if answered wrongly, reset the streak to 0:
        if int(result) == -1:
            db.execute(
                "UPDATE users SET streak = 0 WHERE user_id = ?", currentUserId)

        print("this is result", result)
        return redirect("/")


@app.route("/reset", methods=["POST"])
@login_required
def reset():
    currentUserId = session['user_id']
    print("reset triggered")
    db.execute("UPDATE answers SET answer1 = ?, answer2 = ?, answer3 = ? WHERE user_id = ?",
               0, 0, 0, currentUserId)
    return redirect("/progress")


@app.route("/progress")
@login_required
def progress():
    currentUserId = session['user_id']
    words = db.execute(
        "SELECT * FROM words LEFT OUTER JOIN answers ON words.word_id = answers.word_id WHERE answers.user_id = ?", currentUserId)
    print(words)
    return render_template("/progress.html", words=words)
