var stats = [];
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
        url : "/playerInfo",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify("Sent")
      }).done(function(data) {
        console.log(data[data.length - 2]);
        document.getElementsByTagName("title")[0].innerHTML = "NBA Stats | " + data[data.length - 1];

        if (data[data.length - 3][3] == -1) {
          var tables = document.getElementsByClassName("container")[0];
          while (tables.firstChild) {
            tables.removeChild(tables.firstChild);
          }
          var noData = document.createElement("h1");
          noData.innerHTML = "NO DATA";
          noData.setAttribute("class", "noData")
          tables.appendChild(noData);
        } else {
          const total = document.getElementById("total");
          const average = document.getElementById("average");
          const scoring = document.getElementById("scoring");
          const games = document.getElementById("games");
          var hover = document.getElementsByTagName("tbody");
          document.getElementsByTagName("p")[0].innerHTML = data[data.length - 1];

          document.getElementsByClassName("card-img-top")[0].src = data[data.length - 2][9];
          const texts = document.getElementsByClassName("ml-auto");
          for (var i = 0; i < texts.length; i++) {
            texts[i].innerHTML = data[data.length - 2][i];
          }

          var turnovers = 0;
          for (i = 0; i < data.length - 2; i++) {
            var tr = document.createElement("tr");
            var th = document.createElement("th");
            th.innerHTML = data[i][0];
            th.setAttribute("scope", "row");
            th.setAttribute("class", "align-middle");
  
            var td1 = document.createElement("td");
            var img = document.createElement("img");
            img.setAttribute("class", "logo1");
            img.setAttribute("src", data[i][1]);
            td1.appendChild(img);
  
            var teamName = document.createElement("td");
            teamName.setAttribute("class", "name align-middle");
            teamName.innerHTML = data[i][2];
  
            var td2 = document.createElement("td");
            td2.setAttribute("class", "align-middle");
            td2.innerHTML = data[i][3];
            var td3 = document.createElement("td");
            td3.setAttribute("class", "align-middle");
            td3.innerHTML = data[i][5];
            var td4 = document.createElement("td");
            td4.setAttribute("class", "align-middle");
            td4.innerHTML = data[i][7];
            var td5 = document.createElement("td");
            td5.setAttribute("class", "align-middle");
            td5.innerHTML = data[i][9];
            var td6 = document.createElement("td");
            td6.setAttribute("class", "align-middle");
            td6.innerHTML = data[i][11];
            var td7 = document.createElement("td");
            td7.setAttribute("class", "align-middle");
            td7.innerHTML = data[i][13];
            var td8 = document.createElement("td");
            td8.setAttribute("class", "align-middle");
            td8.innerHTML = data[i][15];
  
            tr.appendChild(th);
            tr.appendChild(td1);
            tr.appendChild(teamName);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            tr.appendChild(td5);
            tr.appendChild(td6);
            tr.appendChild(td7);
            tr.appendChild(td8);
            hover[0].appendChild(tr);
            total.appendChild(hover[0]);
          }
          for (i = 0; i < data.length - 2; i++) {
            var tr = document.createElement("tr");
            var th = document.createElement("th");
            th.innerHTML = data[i][0];
            th.setAttribute("scope", "row");
            th.setAttribute("class", "align-middle");
  
            var td1 = document.createElement("td");
            var img = document.createElement("img");
            img.setAttribute("class", "logo1");
            img.setAttribute("src", data[i][1]);
            td1.appendChild(img);
  
            var teamName = document.createElement("td");
            teamName.setAttribute("class", "name align-middle");
            teamName.innerHTML = data[i][2];
  
            var td2 = document.createElement("td");
            td2.setAttribute("class", "align-middle");
            td2.innerHTML = data[i][4];
            var td3 = document.createElement("td");
            td3.setAttribute("class", "align-middle");
            td3.innerHTML = data[i][6];
            var td4 = document.createElement("td");
            td4.setAttribute("class", "align-middle");
            td4.innerHTML = data[i][8];
            var td5 = document.createElement("td");
            td5.setAttribute("class", "align-middle");
            td5.innerHTML = data[i][10];
            var td6 = document.createElement("td");
            td6.setAttribute("class", "align-middle");
            td6.innerHTML = data[i][12];
            var td7 = document.createElement("td");
            td7.setAttribute("class", "align-middle");
            td7.innerHTML = data[i][14];
            var td8 = document.createElement("td");
            td8.setAttribute("class", "align-middle");
            if (i == data.length - 3) {
              turnovers /= (data.length - 3);
              turnovers = turnovers.toFixed(1);
              td8.innerHTML = turnovers;
            } else {
              turnovers += data[i][16];
              td8.innerHTML = data[i][16];
            }
  
            tr.appendChild(th);
            tr.appendChild(td1);
            tr.appendChild(teamName);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            tr.appendChild(td5);
            tr.appendChild(td6);
            tr.appendChild(td7);
            tr.appendChild(td8);
            hover[1].appendChild(tr);
            average.appendChild(hover[1]);
          }
          for (i = 0; i < data.length - 2; i++) {
            var tr = document.createElement("tr");
            var th = document.createElement("th");
            th.innerHTML = data[i][0];
            th.setAttribute("scope", "row");
            th.setAttribute("class", "align-middle");
  
            var td1 = document.createElement("td");
            var img = document.createElement("img");
            img.setAttribute("class", "logo1");
            img.setAttribute("src", data[i][1]);
            td1.appendChild(img);
  
            var teamName = document.createElement("td");
            teamName.setAttribute("class", "name align-middle");
            teamName.innerHTML = data[i][2];
  
            var td2 = document.createElement("td");
            td2.setAttribute("class", "align-middle");
            td2.innerHTML = data[i][17];
            var td3 = document.createElement("td");
            td3.setAttribute("class", "align-middle");
            td3.innerHTML = data[i][18];
            var td4 = document.createElement("td");
            td4.setAttribute("class", "align-middle");
            td4.innerHTML = data[i][19];
            var td5 = document.createElement("td");
            td5.setAttribute("class", "align-middle");
            td5.innerHTML = data[i][20];
            var td6 = document.createElement("td");
            td6.setAttribute("class", "align-middle");
            td6.innerHTML = data[i][21];
            var td7 = document.createElement("td");
            td7.setAttribute("class", "align-middle");
            td7.innerHTML = data[i][22];
            var td8 = document.createElement("td");
            td8.setAttribute("class", "align-middle");
            td8.innerHTML = data[i][23];
            var td9 = document.createElement("td");
            td9.setAttribute("class", "align-middle");
            td9.innerHTML = data[i][24];
            var td10 = document.createElement("td");
            td10.setAttribute("class", "align-middle");
            td10.innerHTML = data[i][25];
  
            tr.appendChild(th);
            tr.appendChild(td1);
            tr.appendChild(teamName);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            tr.appendChild(td5);
            tr.appendChild(td6);
            tr.appendChild(td7);
            tr.appendChild(td8);
            tr.appendChild(td9);
            tr.appendChild(td10);
            hover[2].appendChild(tr);
            scoring.appendChild(hover[2]);
          }
          for (i = 0; i < data.length - 2; i++) {
            var tr = document.createElement("tr");
            var th = document.createElement("th");
            th.innerHTML = data[i][0];
            th.setAttribute("scope", "row");
            th.setAttribute("class", "align-middle");
  
            var td1 = document.createElement("td");
            var img = document.createElement("img");
            img.setAttribute("class", "logo1");
            img.setAttribute("src", data[i][1]);
            td1.appendChild(img);
  
            var teamName = document.createElement("td");
            teamName.setAttribute("class", "name align-middle");
            teamName.innerHTML = data[i][2];
  
            var td2 = document.createElement("td");
            td2.setAttribute("class", "align-middle");
            td2.innerHTML = data[i][26];
            var td3 = document.createElement("td");
            td3.setAttribute("class", "align-middle");
            td3.innerHTML = data[i][27];
            var td4 = document.createElement("td");
            td4.setAttribute("class", "align-middle");
            td4.innerHTML = data[i][28];
            var td5 = document.createElement("td");
            td5.setAttribute("class", "align-middle");
            td5.innerHTML = data[i][29];
            var td6 = document.createElement("td");
            td6.setAttribute("class", "align-middle");
            td6.innerHTML = data[i][30];
  
            tr.appendChild(th);
            tr.appendChild(td1);
            tr.appendChild(teamName);
            tr.appendChild(td2);
            tr.appendChild(td3);
            tr.appendChild(td4);
            tr.appendChild(td5);
            tr.appendChild(td6);
            hover[3].appendChild(tr);
            games.appendChild(hover[3]);
          }
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
    $("#/standings").click(function() {
      $.ajax({
          type : 'POST',
          url : "/",
          contentType: 'application/json;charset=UTF-8',
          data : JSON.stringify("Sent")
      });
   });
   $("#/scores").click(function() {
    $.ajax({
        type : 'POST',
        url : "/",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify("Sent")
    });
 });
});