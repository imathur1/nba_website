playerNames = [];

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
      url : "/updateNews",
      contentType: 'application/json;charset=UTF-8',
      data : JSON.stringify("Sent")
    }).done(function(data) {
      var group1 = document.getElementsByClassName('row justify-content-around')[0];
      for (var i = 0; i < data[0]; i++) {
        var div = document.createElement("div");
        div.setAttribute('class', 'card col-xs-12 col-sm-12 col-md-10 col-lg-10 col-xl-10');
        let url = data[i + 1][5];
        div.addEventListener('click', function() {
          window.open(url, '_blank');
        });
        var img = document.createElement("img");
        img.setAttribute('class', 'card-img-top');
        img.setAttribute('src', data[i + 1][4]);
        var div2 = document.createElement("div");
        div2.setAttribute('class', 'card-body');
        var h2 = document.createElement("h2");
        h2.setAttribute('class', 'card-title');
        var h5 = document.createElement("h5");
        h5.setAttribute('class', 'card-subtitle mb-3');
        var h6 = document.createElement("h6");
        h6.setAttribute('class', 'card-subtitle mb-2 text-muted');
        var h52 = document.createElement("h5");
        h52.setAttribute('class', 'card-text');

        h2.innerHTML = data[i + 1][0];
        h5.innerHTML = data[i + 1][1];
        h6.innerHTML = data[i + 1][2];
        h52.innerHTML = data[i + 1][3];

        div2.appendChild(h2);
        div2.appendChild(h5);
        div2.appendChild(h6);
        div2.appendChild(h52);
        div.appendChild(img);
        div.appendChild(div2);
        group1.appendChild(div);
      }
      counter = 1;
      index = 5;
      for (var i = data[0]; i < data.length - data[0]; i++) {
        var div = document.createElement("div");
        div.setAttribute('class', 'card card col-xs-12 col-sm-12 col-md-5 col-lg-5 col-xl-5');
        let url = data[i + 1][5];
        div.addEventListener('click', function() {
          window.open(url, '_blank');
        });
        var img = document.createElement("img");
        img.setAttribute('class', 'card-img-top');
        img.setAttribute('src', data[i + 1][4]);
        var div2 = document.createElement("div");
        div2.setAttribute('class', 'card-body');
        var h2 = document.createElement("h2");
        h2.setAttribute('class', 'card-title');
        var h5 = document.createElement("h5");
        h5.setAttribute('class', 'card-subtitle mb-3');
        var h6 = document.createElement("h6");
        h6.setAttribute('class', 'card-subtitle mb-2 text-muted');
        var h52 = document.createElement("h5");
        h52.setAttribute('class', 'card-text');

        h2.innerHTML = data[i + 1][0];
        h5.innerHTML = data[i + 1][1];
        h6.innerHTML = data[i + 1][2];
        h52.innerHTML = data[i + 1][3];

        div2.appendChild(h2);
        div2.appendChild(h5);
        div2.appendChild(h6);
        div2.appendChild(h52);
        div.appendChild(img);
        div.appendChild(div2);
        document.getElementsByClassName('row justify-content-around')[index].appendChild(div);

        if (counter == 2) {
          index += 1;
          counter = 0;
        }
        counter += 1;
      }
    });
});