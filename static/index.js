const auth = "563492ad6f91700001000001630a8169735443afa60bcb18a3770de6";
var wordInfo = word;

function displayWord(wordInfo) {
    document.querySelector("#word").innerHTML = wordInfo.word;
    // document.querySelector("#score ").innerHTML = score;
}

// function to get image with a prompt from pexels api
async function getPhoto(prompt) {
    const data = await fetch(
        `https://api.pexels.com/v1/search?query=${prompt}&per_page=1`,
        {
            method: "GET",
            headers: {
                Accept: "application/json",
                Authorization: auth,
            },
        }
    );
    const result = await data.json();
    let urlWithQuotes = JSON.stringify(result.photos[0].src.medium);
    let photoURL = urlWithQuotes.replace(/["]+/g, '');
    return photoURL;
}


document.addEventListener('DOMContentLoaded', async function () {

    // display the first word
    displayWord(wordInfo);
    var articleList = ["der", "die", "das"];

    // try to get the photo, if fails show a placeholder "image not found" image
    try {
        var photoURL = getPhoto(wordInfo.word);
        document.getElementById("word-image").src = await photoURL;
    } catch (error) {
        console.error(error);
        document.getElementById("word-image").src = "/static/image-not-found.png";
    }


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

            // show the next word button
            document.getElementById("next-word").style.display = "inline-block";

            // fill the result and word_id to hidden elements to be sent to backend with a post request
            document.getElementById("result").value = result;
            document.getElementById("word_id").value = wordInfo.word_id;
        })
    }


})