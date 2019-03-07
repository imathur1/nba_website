const rank1 = document.getElementsByClassName('rank1');
const logo1 = document.getElementsByClassName('logo1');
const name1 = document.getElementsByClassName('name1');
const win1 = document.getElementsByClassName('win1');
const loss1 = document.getElementsByClassName('loss1');
const wp1 = document.getElementsByClassName('wp1');
const gb1 = document.getElementsByClassName('gb1');
const conf1 = document.getElementsByClassName('conf1');
const home1 = document.getElementsByClassName('home1');
const away1 = document.getElementsByClassName('away1');
const last1 = document.getElementsByClassName('last1');
const streak1 = document.getElementsByClassName('streak1');

const rank2 = document.getElementsByClassName('rank2');
const logo2 = document.getElementsByClassName('logo2');
const name2 = document.getElementsByClassName('name2');
const win2 = document.getElementsByClassName('win2');
const loss2 = document.getElementsByClassName('loss2');
const wp2 = document.getElementsByClassName('wp2');
const gb2 = document.getElementsByClassName('gb2');
const conf2 = document.getElementsByClassName('conf2');
const home2 = document.getElementsByClassName('home2');
const away2 = document.getElementsByClassName('away2');
const last2 = document.getElementsByClassName('last2');
const streak2 = document.getElementsByClassName('streak2');

$(document).ready(function(){
    $.ajax({
        type : 'POST',
        url : "/results",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify("Sent")
      }).done(function(data) {
        var standings = data;
        for (var i = 0; i < 15; i++) {
            rank1[i].innerHTML = i + 1;
            logo1[i].src = standings[i][0];
            name1[i].innerHTML = standings[i][1];
            win1[i].innerHTML = standings[i][2];
            loss1[i].innerHTML = standings[i][3];
            wp1[i].innerHTML = standings[i][4];
            gb1[i].innerHTML = standings[i][5];
            conf1[i].innerHTML = standings[i][6];
            home1[i].innerHTML = standings[i][7];
            away1[i].innerHTML = standings[i][8];
            last1[i].innerHTML = standings[i][9];
            streak1[i].innerHTML = standings[i][10];
        }
        for (var i = 0; i < 15; i++) {
            rank2[i].innerHTML = i + 1;
            logo2[i].src = standings[i + 15][0];
            name2[i].innerHTML = standings[i + 15][1];
            win2[i].innerHTML = standings[i + 15][2];
            loss2[i].innerHTML = standings[i + 15][3];
            wp2[i].innerHTML = standings[i + 15][4];
            gb2[i].innerHTML = standings[i + 15][5];
            conf2[i].innerHTML = standings[i + 15][6];
            home2[i].innerHTML = standings[i + 15][7];
            away2[i].innerHTML = standings[i + 15][8];
            last2[i].innerHTML = standings[i + 15][9];
            streak2[i].innerHTML = standings[i + 15][10];
        }  
    });
    $("#/").click(function() {
        $.ajax({
            type : 'POST',
            url : "/",
            contentType: 'application/json;charset=UTF-8',
            data : JSON.stringify("Sent")
        });
    });
    $("#/#upcoming").click(function() {
        $.ajax({
            type : 'POST',
            url : "/",
            contentType: 'application/json;charset=UTF-8',
            data : JSON.stringify("Sent")
        });
    });
});