# Imports titles and genres from CSV into a SQLite database

import cs50
import csv

# # Create database
open("trial2.db", "w").close()
db = cs50.SQL("sqlite:///trial2.db")

# # Create tables
db.execute("CREATE TABLE words(word_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, word TEXT NOT NULL, article TEXT NOT NULL, answer1 INTEGER DEFAULT 0, answer2 INTEGER DEFAULT 0)")

# Open CSV file
with open("words_small.csv", "r") as file:

    # Create DictReader
    reader = csv.DictReader(file)

    # Iterate over CSV file
    for row in reader:
        print(row)
        # Canoncalize title
        word = row["word"]
        article = row["article"]

        # Insert words
        db.execute("INSERT INTO words (word, article) VALUES(?, ?)", word, article)

        # # Insert genres
        # for genre in row["genres"].split(", "):
        #     db.execute("INSERT INTO genres (show_id, genre) VALUES(?, ?)", show_id, genre)