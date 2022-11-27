
var wordInfo = word;

function displayWord(wordInfo) {
    document.querySelector("#word").innerHTML = wordInfo.word;
    // document.querySelector("#score ").innerHTML = score;
}


document.addEventListener('DOMContentLoaded', function () {
    // display the first word
    displayWord(wordInfo);
    var articleList = ["der", "die", "das"];

    for (var i = 0; i < 3; i++) {
        let currentArticle = articleList[i];
        let currentButton = document.getElementById(currentArticle);
        currentButton.addEventListener('click', function () {
            let result = currentArticle.localeCompare(wordInfo.article);
            // user selected correct article
            if (result == 0) {
                console.log(currentArticle, "was correct");
                // change button's color to green
                currentButton.style.backgroundColor = "green";
                // set result value to 1 to make things simpler on backend
                result = 1;
            }


            // user selected wrong article
            else {
                // change button's color to red
                let correctButton = document.getElementById(wordInfo.article);
                correctButton.style.backgroundColor = "green";
                currentButton.style.backgroundColor = "red";
                console.log(currentArticle, "was incorrect");
                // set result value to 0 to make things simpler on backend
                result = 0;
            }


            // disable all buttons
            for (let i = 0; i < 3; i++) {
                let currentArticle = articleList[i];
                let currentButton = document.getElementById(currentArticle);
                currentButton.disabled = true;
            }
            document.getElementById("next-word").style.display = "inline-block";
            document.getElementById("result").value = result;
            document.getElementById("word_id").value = wordInfo.word_id;
        })
    }


})