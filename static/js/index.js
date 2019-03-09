var today = new Date();
var offset = today.getTimezoneOffset() * 60;
year = today.getFullYear();
month = today.getMonth() + 1;
day = today.getDate();
hours = today.getHours();
minutes = today.getMinutes();
if (Number(year) < 10) {
  year = "0" + year;
}
if (Number(month) < 10) {
  month = "0" + month;
}
if (Number(day) < 10) {
  day = "0" + day;
}
if (Number(hours) < 10) {
  hours = "0" + hours;
}
if (Number(minutes) < 10) {
  minutes = "0" + minutes;
}
var date = year + "-" + month + "-" + day + "T" + hours + ":" + minutes + ":00+00:00";
var info = [Number(offset), date];

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

var playerNames = [];

$(document).ready(function(){
  $.ajax({
    type : 'POST',
    url : "/update",
    contentType: 'application/json;charset=UTF-8',
    data : JSON.stringify(info)
  }).done(function(data) {
    var upcoming = data;
    const logos = document.getElementsByClassName("logo");
    const teams = document.getElementsByClassName("team");
    const days = document.getElementsByClassName("day");
    const times = document.getElementsByClassName("time");

    for (var i = 0; i < 6; i++) {
      logos[i * 2].src = upcoming[i][4];
      logos[i * 2 + 1].src = upcoming[i][6];
      teams[i * 2].innerHTML = upcoming[i][3];
      teams[i * 2 + 1].innerHTML = upcoming[i][5];      
      days[i].innerHTML = upcoming[i][1];
      times[i].innerHTML = upcoming[i][2];
    }
  });

  $.ajax({
    type : 'POST',
    url : "/updateAutocomplete",
    contentType: 'application/json;charset=UTF-8',
    data : JSON.stringify("Sent")
  }).done(function(data) {
      playerNames = data;
      autocomplete(document.getElementById("playersID"), playerNames);
  });
});

const carousel = document.getElementsByClassName("c-image");
var players = [
"static/images/players/giannis.jpg",
"static/images/players/curry.jpg",
"static/images/players/lebron.jpg",
"static/images/players/durant.jpg",
"static/images/players/irving.jpg",
"static/images/players/harden.jpg",
"static/images/players/leonard.jpg",
"static/images/players/davis.jpg",
"static/images/players/westbrook.jpg",
"static/images/players/butler.jpeg",
"static/images/players/embiid.jpg",
"static/images/players/doncic.jpg"
];

for (var i = 0; i < carousel.length; i++) {
  var random = Math.floor(Math.random() * players.length);
  carousel[i].src = players[random];
  players.splice(random, 1);
}