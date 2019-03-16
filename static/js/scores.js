var today = new Date();
var offset = today.getTimezoneOffset() * 60;
year = today.getFullYear();
month = today.getMonth() + 1;
day = today.getDate();
document.getElementsByClassName('form-control')[0].placeholder = year;
document.getElementsByClassName('form-control')[1].placeholder = month;
document.getElementsByClassName('form-control')[2].placeholder = day;
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

var links = [];
var other = [];
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
      url : "/recent",
      contentType: 'application/json;charset=UTF-8',
      data : JSON.stringify(info)
    }).done(function(data) {
      const logos = document.getElementsByClassName("logo");
      const teams = document.getElementsByClassName("team");
      const records = document.getElementsByClassName("record");
      const scores = document.getElementsByClassName("score");

      for (var i = 0; i < 6; i++) {
        logos[i * 2].src = data[i][1];
        logos[i * 2 + 1].src = data[i][5];
        teams[i * 2].innerHTML = data[i][0];
        teams[i * 2 + 1].innerHTML = data[i][4];
        records[i * 2].innerHTML = data[i][2];
        records[i * 2 + 1].innerHTML = data[i][6];
        scores[i * 2].innerHTML = data[i][3];
        scores[i * 2 + 1].innerHTML = data[i][7];
        links.push(data[i][8]);
        if (Number(data[i][3]) > data[i][7]) {
          scores[i * 2].style.color = "#FF0043";
        } else if (Number(data[i][3]) < data[i][7]) {
          scores[i * 2 + 1].style.color = "#FF0043";
        }
      }
    });
    $('form').on('submit', function(event) {
      var tables = document.getElementsByClassName("cont2")[0];
      while (tables.firstChild) {
        tables.removeChild(tables.firstChild);
      }
      other = [];

      var year = document.getElementsByClassName('form-control')[0].value;
      var month = document.getElementsByClassName('form-control')[1].value;
      var day = document.getElementsByClassName('form-control')[2].value;
      if (Number(year) < 10) {
        year = "0" + year;
      }
      if (Number(month) < 10) {
        month = "0" + month;
      }
      if (Number(day) < 10) {
        day = "0" + day;
      }
      $.ajax({
        type : 'POST',
        url : "/gameDate",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify(year + month + day)
      }).done(function(data) {
        if (data === "NO GAMES") {
          var noGames = document.createElement('p');
          noGames.setAttribute('class', 'noGames');
          noGames.innerHTML = "NO GAMES";
          var container = document.getElementsByClassName('cont2')[0];
          container.appendChild(noGames);
        } else {
          var cards = [];
          for (var i = 0; i < data.length; i++) {
            var first = document.createElement('div');
            first.setAttribute('class', 'col-3 card cardO rounded');

            var second = document.createElement('div');
            second.setAttribute('class', 'row higher');

            var third = document.createElement('div');
            third.setAttribute('class', 'col-1');

            var fourth = document.createElement('div');
            fourth.setAttribute('class', 'col-4 text-center');
            var sub1 = document.createElement('p');
            sub1.setAttribute('class', 'newScore');
            fourth.appendChild(sub1);

            var fifth = document.createElement('div');
            fifth.setAttribute('class', 'col-2 text-center');
            var sub2 = document.createElement('p');
            sub2.setAttribute('class', 'newDash');
            sub2.innerHTML = "-";
            fifth.appendChild(sub2);

            var sixth = document.createElement('div');
            sixth.setAttribute('class', 'col-4 text-center');
            var sub3 = document.createElement('p');
            sub3.setAttribute('class', 'newScore');
            sixth.appendChild(sub3);

            second.appendChild(third);
            second.appendChild(fourth);
            second.appendChild(fifth);
            second.appendChild(sixth);

            var top = document.createElement('div');
            top.setAttribute('class', 'row top');

            var img1 = document.createElement('div');
            img1.setAttribute('class', 'col-6 align-self-center');
            var actual1 = document.createElement('img');
            actual1.setAttribute('class', 'img-fluid mx-auto d-block newLogo');
            actual1.setAttribute('src', "");
            actual1.setAttribute('height', "50%");
            actual1.setAttribute('width', "50%");
            img1.appendChild(actual1);

            var img2 = document.createElement('div');
            img2.setAttribute('class', 'col-6 align-self-center');
            var actual2 = document.createElement('img');
            actual2.setAttribute('class', 'img-fluid mx-auto d-block newLogo');
            actual2.setAttribute('src', "");
            actual2.setAttribute('height', "50%");
            actual2.setAttribute('width', "50%");
            img2.appendChild(actual2);

            top.appendChild(img1);
            top.appendChild(img2);

            var middle = document.createElement('div');
            middle.setAttribute('class', 'row middle');

            var one = document.createElement('div');
            var two = document.createElement('div');
            var three = document.createElement('div');
            var four = document.createElement('div');

            one.setAttribute('class', 'col-6 text-center');
            two.setAttribute('class', 'col-6 text-center');
            three.setAttribute('class', 'col-6 text-center');
            four.setAttribute('class', 'col-6 text-center');

            var team1 = document.createElement('p');
            var team2 = document.createElement('p');
            var record1 = document.createElement('p');
            var record2 = document.createElement('p');

            team1.setAttribute('class', 'newTeam');
            team2.setAttribute('class', 'newTeam');

            record1.setAttribute('class', 'newRecord text-muted');
            record2.setAttribute('class', 'newRecord text-muted');

            one.appendChild(team1);
            two.appendChild(team2);
            three.appendChild(record1);
            four.appendChild(record2);

            middle.appendChild(one);
            middle.appendChild(two);
            middle.appendChild(three);
            middle.appendChild(four);

            first.appendChild(second);
            first.appendChild(top);
            first.appendChild(middle);

            cards.push(first);
          }
          var container = document.getElementsByClassName('cont2')[0];
          for (var j = 0; j < cards.length; j += 3) {
            var row = document.createElement('div');
            row.setAttribute('class', 'row justify-content-around');
            try {
              row.appendChild(cards[j]);
              row.appendChild(cards[j + 1]);
              row.appendChild(cards[j + 2]);
              container.appendChild(row);
            } catch (err) {
              container.appendChild(row);
            }
          }
          
          const logos = document.getElementsByClassName("newLogo");
          const teams = document.getElementsByClassName("newTeam");
          const records = document.getElementsByClassName("newRecord");
          const scores = document.getElementsByClassName("newScore");
    
          for (var i = 0; i < cards.length; i++) {
            logos[i * 2].src = data[i][1];
            logos[i * 2 + 1].src = data[i][5];
            teams[i * 2].innerHTML = data[i][0];
            teams[i * 2 + 1].innerHTML = data[i][4];
            records[i * 2].innerHTML = data[i][2];
            records[i * 2 + 1].innerHTML = data[i][6];
            scores[i * 2].innerHTML = data[i][3];
            scores[i * 2 + 1].innerHTML = data[i][7];
            other.push(data[i][8]);
            if (Number(data[i][3]) > data[i][7]) {
              scores[i * 2].style.color = "#FF0043";
            } else if (Number(data[i][3]) < data[i][7]) {
              scores[i * 2 + 1].style.color = "#FF0043";
            }
          }
        }
        const otherCards = document.getElementsByClassName('cardO');
        for (let i = 0; i < otherCards.length; i++) {
          otherCards[i].onclick = function() {
            $.ajax({
                type : 'POST',
                url : "/gameID",
                contentType: 'application/json;charset=UTF-8',
                data : JSON.stringify(other[i])
            });
            window.location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/scores/" + other[i] + "/";
          }
        }
      });
      event.preventDefault();
    });
});

const cards = document.getElementsByClassName('card');
for (let i = 0; i < cards.length; i++) {
  cards[i].onclick = function() {
    $.ajax({
        type : 'POST',
        url : "/gameID",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify(links[i])
    });
    window.location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + "/scores/" + links[i] + "/";
  }
}