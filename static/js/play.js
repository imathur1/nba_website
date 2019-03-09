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
        stats = data;
        console.log(data);
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
});