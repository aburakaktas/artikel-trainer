CREATE TABLE sqlite_sequence(name, seq);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE transactions(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    company_name TEXT NOT NULL,
    share INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE portfolio(
    portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    share INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE words(
    word_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    word_de TEXT NOT NULL,
    article TEXT NOT NULL,
    word_en TEXT,
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    streak INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE answers(
    user_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    answer1 INTEGER DEFAULT 0,
    answer2 INTEGER DEFAULT 0,
    answer3 INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (word_id) REFERENCES words (word_id)
);

SELECT *
FROM words
WHERE word_id IS NOT (SELECT word_id
        FROM
            answers
        WHERE
            answer1 = 1
            AND answer2 = 1
            AND answer3 = 1
    )
ORDER BY
    RANDOM()
LIMIT
    1;


SELECT * FROM words WHERE word_id IS NOT (SELECT word_id FROM answers WHERE answer1 = 1 AND answer2 = 1 AND answer3 = 1) ORDER BY RANDOM() LIMIT 1;