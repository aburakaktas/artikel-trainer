# Artikel trainer
*This is my final project submission for [CS50](https://cs50.harvard.edu/x).*

**Video demo:** 



[![a](https://img.youtube.com/vi/ak5ia7yuUo8/maxresdefault.jpg)](https://www.youtube.com/watch?v=ak5ia7yuUo8)

https://www.youtube.com/watch?v=ak5ia7yuUo8


---

<br>

**Description:**

Artikel trainer is a web application for German learners. In German, all nouns have a gender: masculine(der), feminine(die), or neuter(das). These are also called "artikels" in German. It is essential to learn the genders of the nouns to form correct sentences. Even though there are some rules of thumb, it comes down to memorizing them.

Artikel trainer makes the genders of German nouns easy to learn with a quiz game interface. The app aims to stimulate visual memory by showing images related to the words displayed. It also tracks users' progress to make sure they memorize the genders of nouns.

Here is how the main functionality of the app works:
- The user creates a new account to use the app.
- The app displays a random German noun accompanied by an image and an English translation. 
- After that, the app waits for the user to select the correct artikel of the noun: "Der", "Die" or "Das".
- User selects the answer they think is correct. If the answer was correct, the selected option turns green. If the answer was wrong, the selected option turns red, and the correct option turns green.
- "Next word" button appears. When the user clicks on it, the app shows a new random word.
- This loop continues until the user answers all the nouns correctly. If a noun is already answered correctly three times in a row, the app will not show it again, marking it as learned.
- The "Streak" tag shows how many times the user answered correctly in a row.
- The "Fully practiced" tag shows how many nouns are marked as learned, as well as the total number of nouns available.
- At any time, the user can go to the "Progress" page to see their progress. On this page, the app displays the last three answers for every noun. The user can choose to reset their progress with the "Reset progress" button, displayed at the end of the word list.

Here are some technical details about the app:
- Backend is written in Python using [Flask](https://flask.palletsprojects.com/en/2.2.x/), and [SQLite](https://www.sqlite.org/index.html) for database.
- Frontend is written in pure Javascript. [Tailwind CSS](https://tailwindcss.com/) is used for styling.
- UX / UI Design is done in [Figma](https://www.figma.com/).
- Photos provided by [Pexels](https://www.pexels.com/) using their free image API.
- The words in the database are collected from [this public GitHub repository](https://github.com/patsytau/anki_german_a1_vocab).

Explanation of files in the project:
- [app.py](/app.py): Flask app. It has all the routes, manipulates the database based on inputs coming with GET and POST requests, and serves information to the frontend.
- [game.db](/game.db): The database. It stores auth information, the words, and the user's answers.
- [static/index.js](/static/index.js): The script for the main game interface. It displays the word data it got from the backend, makes an async request to Pexels image API to get an image related to the word, manipulates the DOM when the user selects an answer, and finally sends the answer data to the backend.
- [templates](/templates/): HTML pages. Utilizes [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) when necessary. The pages are fully responsive.
- [static/css](static/css/): Tailwind CSS. Also, the font [Inter](https://rsms.me/inter/) is added here.
- [dbimporter.py](misc/dbimporter.py): The custom Python script to collect the Goethe Institute A1 level German vocabulary list from the TSV file found in [this public GitHub repository](https://github.com/patsytau/anki_german_a1_vocab) from @patsytau.

Some design decisions that changed over the development of this project:
- I initially started writing the whole app logic only in frontend, but after a couple of tries, I realized it made sense to move the logic related to database communication and overall handling of general logic to the backend. The only logic that would stay in frontend would be the time user interacts with a single word. This approach made things much tidier and easy to scale with the introduction of sign-in features.
- I initially used Bootstrap CSS but realized it is limiting me a lot. I created my own designs from scratch using Figma and installed Tailwind CSS to develop exactly what I designed. It was somewhat of a challenge to learn Tailwind, but I'd say it was one of the most rewarding things for me to be able to develop the UI exactly how I wanted.
- One feature I struggled with for some time was making a request to Pexels image API. The main problem was it usually took some time to get the image data back from the API, and I had to use async requests to get the image to show on screen, which I did not know how it worked. After a couple of tutorials later, I managed to make it work.
- The full history of the project development is also in this repository as I used git from day one to document my process with (mostly) clear commit notes.

Next steps:
- App currently only supports the nouns from A1 level. More levels can be added.
- The handling of authentication errors can be moved to the frontend with Ajax. Right now it is using the "apology" logic written by the CS50 team.


Thanks:
- CS50 team for the amazing course
- Ludwig for the inspiration