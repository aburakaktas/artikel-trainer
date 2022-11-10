var id = 1;
var score = 0;
var wordInfo = getWordInfo(words, id);

// get word info by providing the words array and a word id
function getWordInfo(arr, id) {
    for (var i = 0, len = arr.length; i < len; i++) {
        if (arr[i].word_id == id) {
            return arr[i];
        }
    }
}

function displayWord(wordInfo) {

    document.querySelector("#word").innerHTML = wordInfo.word;
}


document.addEventListener('DOMContentLoaded', function () {
    console.log(words);

    // display the first word
    
    displayWord(wordInfo);

    // get buttons
    derButton = document.getElementById("der");
    dieButton = document.getElementById("die");
    dasButton = document.getElementById("das");



    // event listener for buttons
    // DAS
    dasButton.addEventListener('click', function () {
        var result = "das".localeCompare(wordInfo.article);
        console.log(result);
        if (result == 0) {
            console.log("Das was correct");
            score++;
        }
        else {
            console.log("Das was incorrect");
        }
        id++;
        displayWord(getWordInfo(words, id));
    });
})