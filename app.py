from flask import Flask, redirect, render_template, request
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///misc/trial2.db")



@app.route("/", methods=["GET", "POST"])

def index():
    word = db.execute("SELECT * FROM words WHERE answer1 = ? OR answer2 = ? ORDER BY RANDOM() LIMIT 1", 0, 0)[0]
    
    if request.method == "GET":
        
        print("inside get:", word)
        return render_template("index.html", word=word)
        
    else:
        print("inside post:", word)
        result = request.form.get("result")
        wordId = request.form.get("word_id")
        # if user answered correctly, write the answer to database
        if result == '1':
            # get the answer 1 and move it to answer 2
            answer1 = db.execute("SELECT * FROM words WHERE word_id = ?", wordId)[0]['answer1']
            print("answer1:", answer1)
            db.execute("UPDATE words SET answer2 = ? WHERE word_id = ?", answer1, wordId)
            # overwrite answer 1 with new answer
            db.execute("UPDATE words SET answer1 = ? WHERE word_id = ?", int(result), wordId)
            
        print("this is result", result)
        return redirect("/")
