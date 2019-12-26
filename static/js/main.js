function slider_update(val) {
    var text;
    if (val == 1){
        text = " follow"
    } else {
        text = " follows"
    }
    document.getElementById("label1").innerHTML = val + text;
}

function slider_update_unfollow(val) {
    text = 'Skip above '
    document.getElementById("label1").innerHTML = text + val + ',000 followers.';
}

function slider_update_likes(val) {
    var text;
    if (val == 1){
        text = " like"
    } else {
        text = " likes"
    }
    document.getElementById("label1").innerHTML = val + text;
}

function block_input(){
    var value = document.getElementById('dropdown').value;
    if (value == "1") {
        document.getElementById('skip_above').disabled = true;
        document.getElementById("label1").innerHTML = 'Skip above?';
    } else {
        document.getElementById('skip_above').disabled = false;
    }
}

function validateFormFollow() {
    var hashtag = document.forms[''][''].value;
    if (hashtag == '') {
        alert('You need to provide a hastag to start following!');
            return false;
    }
}

function displayWaitGif() {
    document.getElementById('loading').style.visibility = "visible";
}