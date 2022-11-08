var n = 1;
var score = 0;
var wrongScore = 0;
// var correctArticle = words[n].article;

function checkArticle() { }

document.addEventListener('DOMContentLoaded', function () {
    console.log(words);

    // get word and article by providing the words array and a word id
    function getWordAndArticle(arr, id) {
        for (var i = 0, len = arr.length; i < len; i++) {
            if (arr[i].word_id == id) {
                return arr[i];
            }
        }
    }

    // get word by word id
    function getWordByWordId(arr, value) {

        for (var i = 0, iLen = arr.length; i < iLen; i++) {

            if (arr[i].word_id == value) return arr[i].word;
        }
    }


    // display the first word
    currentWord = getWordAndArticle(words, n).word;
    currentId = getWordAndArticle(words, n).word_id;
    console.log(currentWord);
    document.querySelector("#word").innerHTML = currentWord + " " + currentId;

    // get buttons
    derButton = document.getElementById("der");
    dieButton = document.getElementById("die");
    dasButton = document.getElementById("das");

    // checks if article was correct. Returns true if correct and false if not
    function checkArticle(atc) {
        console.log(atc + "clicked");
        if (correctArticle.localeCompare(atc) == 0) {
            return true;
        }
        else {
            return false;
        }
    }

    //
    function getNextWord(result) {
        if (result) {
            score++;
        }
        n++;
        document.querySelector("#word").innerHTML = words[n].word;
        document.querySelector("#score").innerHTML = score;
        correctArticle = words[n].article;
    }

    // event listener for buttons
    // DAS
    dasButton.addEventListener('click', function () {
        result = checkArticle("das");
        if (result) {
            console.log("Das was correct");
        }
        else {
            console.log("Das was incorrect");
        }
        getNextWord(result);
    });
})