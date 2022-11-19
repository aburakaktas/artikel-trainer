
var wordInfo = word;
var answers = {};

function displayWord(wordInfo) {
    document.querySelector("#word").innerHTML = wordInfo.word;
    // document.querySelector("#score ").innerHTML = score;
}


document.addEventListener('DOMContentLoaded', function () {
    // display the first word
    displayWord(wordInfo);


    dasButton = document.getElementById("das");
    dasButton.addEventListener('click', function () {
        var result = "das".localeCompare(wordInfo.article);
        console.log(result);
        if (result == 0) {
            console.log("Das was correct");
            dasButton.style.backgroundColor = ('green');
            // dasButton.style.transition = "all 2s"
            answers[wordInfo.word_id] = "true";
            result = 1;
        }
        else {
            console.log("Das was incorrect");
            document.getElementById("das").style.backgroundColor = ('red');
            answers[wordInfo.word_id] = "false";
            result = 0;
        }
        document.getElementById("result").value = result;
        document.getElementById("word_id").value = wordInfo.word_id;
    });

    


})