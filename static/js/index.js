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
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/      
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;

      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      var count = 0;
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase() && count < 4) {
          count += 1;
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
              $('.search__field').focus();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) {
            x[currentFocus].click();
            $.ajax({
              type : 'POST',
              url : "/players",
              contentType: 'application/json;charset=UTF-8',
              data : JSON.stringify($("#players").val())
            }).done(function(data) {
              window.location = "/playerStats/" + data + "/";
            });
          };
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
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
    playerNames = upcoming[upcoming.length - 1];
    autocomplete(document.getElementById("players"), playerNames);
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

  $("#standings").click(function() {
    $.ajax({
      type : 'POST',
      url : "/standings",
      contentType: 'application/json;charset=UTF-8',
      data : JSON.stringify("Sent")
    });
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