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