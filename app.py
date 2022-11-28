from flask import Flask, redirect, render_template, request
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///game.db")



@app.route("/", methods=["GET", "POST"])
def index():
    wordList = db.execute("SELECT * FROM words WHERE answer1 = ? OR answer2 = ? OR answer3 = ? ORDER BY RANDOM() LIMIT 1", 0, 0, 0)
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
        answer2 = db.execute("SELECT * FROM words WHERE word_id = ?", wordId)[0]['answer2']
        db.execute("UPDATE words SET answer3 = ? WHERE word_id = ?", answer2, wordId)
        
        # get the answer 1 and move it to answer 2
        answer1 = db.execute("SELECT * FROM words WHERE word_id = ?", wordId)[0]['answer1']
        db.execute("UPDATE words SET answer2 = ? WHERE word_id = ?", answer1, wordId)
        
        # overwrite answer 1 with new answer
        db.execute("UPDATE words SET answer1 = ? WHERE word_id = ?", int(result), wordId)
            
        print("this is result", result)
        return redirect("/")

@app.route("/reset", methods=["POST"])
def reset():
    print("reset triggered")
    db.execute("UPDATE words SET answer1 = ?, answer2 = ?", 0, 0)
    return redirect("/progress")

@app.route("/progress")
def progress():
    words = db.execute("SELECT * FROM words")
    # print(words)
    return render_template("/progress.html", words = words)
