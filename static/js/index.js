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

$('#myModal').modal({show: false});

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
window.addEventListener('mouseup', function(e) {
  if (typeof e === 'object') {
    if (e.which == 2) {
      closeAllLists2();
    }
  }
});
}

var playerNames = [];
var preview = [];
$(document).ready(function(){
  var rand = Math.random();
  if (rand <= (1 / 3)) {
    $('#myModal2').modal('show');
  }
  $.ajax({
    type : 'POST',
    url : "/update",
    contentType: 'application/json;charset=UTF-8',
    data : JSON.stringify(info)
  }).done(function(data) {
    if (data === "Season Over") {
      var container = document.getElementsByClassName('container-fluid');
      while (container.firstChild) {
        container.removeChild(container.firstChild);
      }
      var seasonOver = document.createElement("h1");
      seasonOver.innerHTML = "Season Over";
      seasonOver.setAttribute("class", "seasonOver")
      container.appendChild(seasonOver);
    } else {
      preview = data[data.length - 1];
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
"https://cdn.nba.net/nba-drupal-prod/styles/landscape/s3/2017-10/20171021_GIANNIS.jpg?itok=DyZjKsHL",
"https://cdn.nba.net/nba-drupal-prod/styles/landscape/s3/2018-11/stephen-curry-shoots-pose-iso-1107.jpg?itok=5BEWJZoQ",
"https://cdn.nba.net/nba-drupal-prod/styles/landscape/s3/2018-10/lebron_dunk.jpg?itok=vqzWCrFw",
"https://cdn.nba.net/nba-drupal-prod/styles/landscape/s3/2017-08/durant-celebrates-finals.jpg?itok=gvt_aiWz",
"http://images.performgroup.com/di/library/omnisport/3a/ff/kyrieirving-cropped_6kd1csejc48n1psgtc4py4dno.jpg?t=1182393929",
"https://images.axios.com/8wUansaUjDMYzmt8t2qLSXMa5rM=/0x71:4269x2472/1920x1080/2019/02/11/1549849055985.jpg",
"https://nssdata.s3.amazonaws.com/images/galleries/18429/kawhi-leonard-110318-ftr-gettyjpg-t12l29gx1ont10g3s2nvbqbrn.jpg",
"https://s.yimg.com/uu/api/res/1.2/Ezf7oPM7Ek3Bh1jp7RvQTw--~B/aD0xMDgwO3c9MTkyMDtzbT0xO2FwcGlkPXl0YWNoeW9u/http://media.zenfs.com/en-GB/homerun/omnisport.uk/00ec56829389c8474af529a07ed2ef50",
"https://a.espncdn.com/combiner/i?img=%2Fmedia%2Fmotion%2F2018%2F1207%2Fdm_181207_nba_76ers_butler_sotfull%2Fdm_181207_nba_76ers_butler_sotfull.jpg",
"https://cdn.nba.net/nba-drupal-prod/styles/landscape/s3/2017-11/EMBIID%20PP.jpg?itok=jIgfw7N6",
"https://images.performgroup.com/di/library/NBA_Global_CMS_image_storage/f8/40/luka-doncic-2-012119-ftr-gettyjpg_fblns1vpdkjz1thjkjzs6uprh.jpg?t=1913837288&quality=100"
];

for (var i = 0; i < carousel.length; i++) {
  var random = Math.floor(Math.random() * players.length);
  carousel[i].src = players[random];
  players.splice(random, 1);
}

cards = document.getElementsByClassName("card");
for (let i = 0; i < cards.length; i++) {
  cards[i].onclick = function() {
    var body = document.getElementsByClassName('modal-body')[0];
    while (body.firstChild) {
      body.removeChild(body.firstChild);
    }
    if (preview[i] == "Error") {
      var h1 = document.createElement("h1");
      h1.innerHTML = "No Article :(";
      body.appendChild(h1);
    } else {      
      var h1 = document.createElement("h1");
      h1.innerHTML = preview[i][0];
      body.appendChild(h1);
      for (var j = 2; j < preview[i].length; j++) {
        var p = document.createElement("p");
        p.innerHTML = preview[i][j];
        if (j == preview[i].length - 1) {
          if (p.innerHTML.charAt(0) === "-") {
            p.innerHTML = "- " + p.innerHTML.substr(2);
          }
          p.setAttribute('class', 'bottomO');
        }
        body.appendChild(p);
      }
    }
    $('#myModal').modal('show');
  }
}