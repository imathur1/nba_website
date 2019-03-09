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

var playerNames = [];

function autocomplete(inp, arr) {
  var currentFocus;    
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      this.parentNode.appendChild(a);
      var count = 0;
      for (i = 0; i < arr.length; i++) {
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase() && count < 8) {
          count += 1;
          b = document.createElement("DIV");
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          b.addEventListener("click", function(e) {
            inp.value = this.getElementsByTagName("input")[0].value;
            $.ajax({
              type : 'POST',
              url : "/playerName",
              contentType: 'application/json;charset=UTF-8',
              data : JSON.stringify($("#playersID").val())
            });
            var s = $("#playersID").val();
            s = s.replace(" ", "-");
            var index = s.indexOf("/");
            var loc = ""
            for (var i = 0; i < index; i++) {
              loc += window.location.hostname[i];
            }
            window.location = loc + "/players/" + s + "/";
          });
          a.appendChild(b);
        }
      }
  });

  inp.addEventListener("keydown", function(e) {
    if (e.keyCode == 13) {
      e.preventDefault();
    }
  });

  function closeAllLists(elmnt) {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  function closeAllLists2() {
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {  
      x[i].parentNode.removeChild(x[i]);
    }
  }
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
$(window).blur(function() {
  closeAllLists2();
});
}

$(document).ready(function(){
    $.ajax({
        type : 'POST',
        url : "/updateAutocomplete",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify("Sent")
      }).done(function(data) {
        playerNames = data;
        autocomplete(document.getElementById("playersID"), playerNames);
    });

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