from flask import Flask, redirect, render_template, request
from cs50 import SQL

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///misc/trial.db")



@app.route("/", methods=["GET", "POST"])

def index():
    words = db.execute("SELECT * FROM words")
    return render_template("index.html", words=words)
