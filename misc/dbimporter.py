import cs50
import csv
import re

# debug flag
debugMode = False

# Create database
if not debugMode:
    open("game.db", "w").close()
    db = cs50.SQL("sqlite:///game.db")

# Create tables
if not debugMode:
    db.execute("CREATE TABLE words(word_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, word_de TEXT NOT NULL, article TEXT NOT NULL, word_en TEXT)")
    db.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,username TEXT NOT NULL,hash TEXT NOT NULL,streak INTEGER NOT NULL DEFAULT 0);")
    db.execute("CREATE TABLE answers(user_id INTEGER NOT NULL,word_id INTEGER NOT NULL,answer1 INTEGER DEFAULT 0,answer2 INTEGER DEFAULT 0,answer3 INTEGER DEFAULT 0,FOREIGN KEY (user_id) REFERENCES users (user_id),FOREIGN KEY (word_id) REFERENCES words (word_id));")

# Open CSV file
with open("raw_csv_txt_files/a1wordsraw.csv", "r") as file:
    
    # Create DictReader
    reader = csv.DictReader(file)
    articleList = ["der", "die", "das"]

    for row in reader:
        word_de_raw = row["word-de"]
        for article in articleList:
            match = re.findall(f"(^{article})\s([a-zA-Z0-9äöüÄÖÜßé-]*)", word_de_raw)
            if not match:
                continue
            
            word_de = match[0][1]
            word_en = row["word-en"].capitalize()
            
            # Insert words
            if not debugMode:
                if not db.execute("SELECT * FROM words WHERE word_de = ?", word_de):
                    db.execute("INSERT INTO words (word_de, article, word_en) VALUES(?, ?, ?)", word_de, article, word_en)

