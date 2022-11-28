# Imports titles and genres from CSV into a SQLite database

import cs50
import csv
import re


# # # Create database
open("game.db", "w").close()
db = cs50.SQL("sqlite:///game.db")

# # # Create tables
db.execute("CREATE TABLE words(word_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, word_de TEXT NOT NULL, article TEXT NOT NULL, word_en TEXT, answer1 INTEGER DEFAULT 0, answer2 INTEGER DEFAULT 0, answer3 INTEGER DEFAULT 0)")

# Open CSV file
with open("a1wordsraw.csv", "r") as file:

    # Create DictReader
    reader = csv.DictReader(file)

    articleList = ["der", "die", "das"]

    for row in reader:
        word_de_raw = row["word-de"]
        for article in articleList:
            match = re.findall(f"(^{article})\s([a-zA-Z0-9äöüÄÖÜß]*)", word_de_raw)
            if not match:
                continue
            print(article, match[0][0], match[0][1])
            word_de = match[0][1]
            word_en = row["word-en"]
            # Insert words
            if not db.execute("SELECT * FROM words WHERE word_de = ?", word_de):
                db.execute("INSERT INTO words (word_de, article, word_en) VALUES(?, ?, ?)", word_de, article, word_en)

