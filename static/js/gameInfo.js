var playerNames = [];
var recap = "";
var allData = [];
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
        url : "/gameUpdate",
        contentType: 'application/json;charset=UTF-8',
        data : JSON.stringify("Sent")
      }).done(function(data) {
        allData = data;
        if (data === "NO DATA") {
            var tables = document.getElementsByClassName("container")[0];
            while (tables.firstChild) {
              tables.removeChild(tables.firstChild);
            }
            var noData = document.createElement("h1");
            noData.style.height = Number(screen.height * 0.6) + "px";
            noData.innerHTML = "NO DATA";
            noData.setAttribute("class", "noData")
            tables.appendChild(noData);
        } else {
            recap = data[data.length - 1];
            var logo = document.getElementsByClassName('logo');
            logo[0].src = data[1][1];
            logo[1].src = data[2][1];
            var score = document.getElementsByClassName('score');
            score[0].innerHTML = data[1][5];
            score[1].innerHTML = data[2][5];
    
            var quote = document.getElementsByClassName('quote')[0];
            quote.innerHTML = data[0][2];

            if (Number(data[1][5]) > Number(data[2][5])) {
                score[0].style.color = "#007bff";
            } else if (Number(data[1][5]) < Number(data[2][5])) {
                score[1].style.color = "#007bff";
            }
    
            var name = document.getElementsByClassName('name');
            name[0].innerHTML = data[1][0];
            name[1].innerHTML = data[2][0];
            var record = document.getElementsByClassName('record');
            record[0].innerHTML = data[1][4];
            record[1].innerHTML = data[2][4];
            var event = document.getElementsByClassName('event');
            event[0].innerHTML = data[0][0];
            event[1].innerHTML = data[0][1];
    
            var title = document.getElementsByTagName('title')[0];
            title.innerHTML = "NBA Stats | " + data[1][3] + " v. " + data[2][3];
            var quarterHead = document.getElementById('quarterHead');
            var t1 = document.getElementById('t1');
            var t2 = document.getElementById('t2');
            var miniLogo = document.getElementsByClassName('miniLogo');
            var teamName = document.getElementsByClassName('left');
            miniLogo[0].src = data[1][2];
            miniLogo[1].src = data[2][2];
            teamName[0].innerHTML = data[1][0];
            teamName[1].innerHTML = data[2][0];
    
            var quarters1 = data[1][6];
            var quarters2 = data[2][6];
            var overtime = 1;
            for (var i = 0; i < quarters1.length; i++) {
                var th = document.createElement('th');
                th.setAttribute('scope', 'col');
                if (i >= 4) {
                    th.innerHTML = "OT" + overtime;
                    overtime += 1;
                } else {
                    th.innerHTML = "Q" + (i + 1);
                }
                quarterHead.appendChild(th);
                var one = document.createElement('th');
                one.setAttribute('class', 'align-middle');
                one.innerHTML = quarters1[i];
                t1.appendChild(one);
                var two = document.createElement('th');
                two.setAttribute('class', 'align-middle');
                two.innerHTML = quarters2[i];
                t2.appendChild(two);
            }
            var th = document.createElement('th');
            th.setAttribute('scope', 'col');
            th.innerHTML = "T";
            quarterHead.appendChild(th);
            var total1 = document.createElement('th');
            total1.setAttribute('class', 'align-middle');
            total1.innerHTML = data[1][5];
            t1.appendChild(total1);
            var total2 = document.createElement('th');
            total2.setAttribute('class', 'align-middle');
            total2.innerHTML = data[2][5];
            t2.appendChild(total2);

            var first = document.getElementsByClassName('first');
            first[0].style.height = Number(data[1][31]) * 3 + "px";
            first[1].style.height = Number(data[1][32]) * 3 + "px";
            first[2].style.height = Number(data[1][33]) * 3 + "px";
            var second = document.getElementsByClassName('second');
            second[0].style.height = Number(data[2][31]) * 3 + "px";
            second[1].style.height = Number(data[2][32]) * 3 + "px";
            second[2].style.height = Number(data[2][33]) * 3 + "px";
            if (Number(data[1][31]) > Number(data[2][31])) {
                first[0].style.backgroundColor = "#007bff";
            } else if (Number(data[1][31]) < Number(data[2][31])) {
                second[0].style.backgroundColor = "#007bff";
            } else {
                first[0].style.backgroundColor = "#007bff";
                second[0].style.backgroundColor = "#007bff";
            }
            if (Number(data[1][32]) > Number(data[2][32])) {
                first[1].style.backgroundColor = "#007bff";
            } else if (Number(data[1][32]) < Number(data[2][32])) {
                second[1].style.backgroundColor = "#007bff";
            } else {
                first[1].style.backgroundColor = "#007bff";
                second[1].style.backgroundColor = "#007bff";
            }
            if (Number(data[1][33]) > Number(data[2][33])) {
                first[2].style.backgroundColor = "#007bff";
            } else if (Number(data[1][33]) < Number(data[2][33])) {
                second[2].style.backgroundColor = "#007bff";
            } else {
                first[2].style.backgroundColor = "#007bff";
                second[2].style.backgroundColor = "#007bff";
            }

            var buttons = document.getElementsByClassName('flip');
            buttons[0].setAttribute('class', 'flip btn btn-lg btn-primary');
            buttons[1].setAttribute('class', 'flip btn btn-lg border-dark');
            var images = document.getElementsByClassName('img1');
            images[0].src = data[1][2];
            images[1].src = data[2][2];

            var big = document.getElementsByClassName('big');
            big[0].innerHTML = data[0][3];
            big[1].innerHTML = data[0][4];
            if (Number(data[0][5]) < 10) {
                data[0][5] = "0" + data[0][5];
            }
            if (Number(data[0][6]) < 10) {
                data[0][6] = "0" + data[0][6];
            }
            big[2].innerHTML = data[0][5];
            big[3].innerHTML = data[0][6];

            var inner = document.getElementsByClassName('inner');
            inner[0].innerHTML = data[1][14] + "/" + data[1][15];
            inner[1].innerHTML = data[1][16] + "%";
            inner[2].innerHTML = data[1][17] + "/" + data[1][18];
            inner[3].innerHTML = data[1][19] + "%";
            inner[4].innerHTML = data[1][20] + "/" + data[1][21];
            inner[5].innerHTML = data[1][22] + "%";

            var circles = document.getElementsByTagName('circle');
            circles[1].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(data[1][16])) / 100 + "px");
            circles[3].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(data[1][19])) / 100 + "px");
            circles[5].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(data[1][22])) / 100 + "px");

            var playersTable = document.getElementById('playersTable');
            for (var i = 0; i < data[1][data[1].length - 1].length; i++) {
                player = data[1][data[1].length - 1][i];
                var tr = document.createElement('tr');
                var position = document.createElement('td');
                position.setAttribute('scope', 'row');
                position.setAttribute('class', 'align-middle');
                position.innerHTML = player[2];
                var name = document.createElement('td');
                name.setAttribute('class', 'align-middle text-left');
                name.innerHTML = player[0];
                var min = document.createElement('td');
                min.setAttribute('class', 'align-middle');
                min.innerHTML = player[3];
                var pt = document.createElement('td');
                pt.setAttribute('class', 'align-middle');
                pt.innerHTML = player[1];

                var fgm = document.createElement('td');
                fgm.setAttribute('class', 'align-middle');
                fgm.innerHTML = player[4];
                var fga = document.createElement('td');
                fga.setAttribute('class', 'align-middle');
                fga.innerHTML = player[5];
                var fgp = document.createElement('td');
                fgp.setAttribute('class', 'align-middle');
                fgp.innerHTML = player[6];

                var ftm = document.createElement('td');
                ftm.setAttribute('class', 'align-middle');
                ftm.innerHTML = player[7];
                var fta = document.createElement('td');
                fta.setAttribute('class', 'align-middle');
                fta.innerHTML = player[8];
                var ftp = document.createElement('td');
                ftp.setAttribute('class', 'align-middle');
                ftp.innerHTML = player[9];

                var tpm = document.createElement('td');
                tpm.setAttribute('class', 'align-middle');
                tpm.innerHTML = player[10];
                var tpa = document.createElement('td');
                tpa.setAttribute('class', 'align-middle');
                tpa.innerHTML = player[11];
                var tpp = document.createElement('td');
                tpp.setAttribute('class', 'align-middle');
                tpp.innerHTML = player[12];

                var oreb = document.createElement('td');
                oreb.setAttribute('class', 'align-middle');
                oreb.innerHTML = player[13];
                var dreb = document.createElement('td');
                dreb.setAttribute('class', 'align-middle');
                dreb.innerHTML = player[14];
                var reb = document.createElement('td');
                reb.setAttribute('class', 'align-middle');
                reb.innerHTML = player[15];

                var ast = document.createElement('td');
                ast.setAttribute('class', 'align-middle');
                ast.innerHTML = player[16];
                var stl = document.createElement('td');
                stl.setAttribute('class', 'align-middle');
                stl.innerHTML = player[17];
                var tov = document.createElement('td');
                tov.setAttribute('class', 'align-middle');
                tov.innerHTML = player[18];
                var blk = document.createElement('td');
                blk.setAttribute('class', 'align-middle');
                blk.innerHTML = player[19];
                var pf = document.createElement('td');
                pf.setAttribute('class', 'align-middle');
                pf.innerHTML = player[20];

                tr.appendChild(position);
                tr.appendChild(name);
                tr.appendChild(min);
                tr.appendChild(pt);
                tr.appendChild(fgm);
                tr.appendChild(fga);
                tr.appendChild(fgp);
                tr.appendChild(ftm);
                tr.appendChild(fta);
                tr.appendChild(ftp);
                tr.appendChild(tpm);
                tr.appendChild(tpa);
                tr.appendChild(tpp);
                tr.appendChild(oreb);
                tr.appendChild(dreb);
                tr.appendChild(reb);
                tr.appendChild(ast);
                tr.appendChild(stl);
                tr.appendChild(tov);
                tr.appendChild(blk);
                tr.appendChild(pf);
                playersTable.appendChild(tr);
            }
        }
    });
});

var buttons = document.getElementsByClassName('flip');
buttons[0].onclick = function() {
    if (!(buttons[0].className === 'flip btn btn-lg btn-primary')) {
        buttons[0].setAttribute('class', 'flip btn btn-lg btn-primary');
        buttons[1].setAttribute('class', 'flip btn btn-lg border-dark');
        var playersTable = document.getElementById('playersTable');
        while (playersTable.firstChild) {
            playersTable.removeChild(playersTable.firstChild);
        }
        
        var circles = document.getElementsByTagName('circle');
        circles[1].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(allData[1][16])) / 100 + "px");
        circles[3].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(allData[1][19])) / 100 + "px");
        circles[5].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(allData[1][22])) / 100 + "px");
        var inner = document.getElementsByClassName('inner');
        inner[0].innerHTML = allData[1][14] + "/" + allData[1][15];
        inner[1].innerHTML = allData[1][16] + "%";
        inner[2].innerHTML = allData[1][17] + "/" + allData[1][18];
        inner[3].innerHTML = allData[1][19] + "%";
        inner[4].innerHTML = allData[1][20] + "/" + allData[1][21];
        inner[5].innerHTML = allData[1][22] + "%";
        for (var i = 0; i < allData[1][allData[1].length - 1].length; i++) {
            player = allData[1][allData[1].length - 1][i];
            var tr = document.createElement('tr');
            var position = document.createElement('td');
            position.setAttribute('scope', 'row');
            position.setAttribute('class', 'align-middle');
            position.innerHTML = player[2];
            var name = document.createElement('td');
            name.setAttribute('class', 'align-middle text-left');
            name.innerHTML = player[0];
            var min = document.createElement('td');
            min.setAttribute('class', 'align-middle');
            min.innerHTML = player[3];
            var pt = document.createElement('td');
            pt.setAttribute('class', 'align-middle');
            pt.innerHTML = player[1];

            var fgm = document.createElement('td');
            fgm.setAttribute('class', 'align-middle');
            fgm.innerHTML = player[4];
            var fga = document.createElement('td');
            fga.setAttribute('class', 'align-middle');
            fga.innerHTML = player[5];
            var fgp = document.createElement('td');
            fgp.setAttribute('class', 'align-middle');
            fgp.innerHTML = player[6];

            var ftm = document.createElement('td');
            ftm.setAttribute('class', 'align-middle');
            ftm.innerHTML = player[7];
            var fta = document.createElement('td');
            fta.setAttribute('class', 'align-middle');
            fta.innerHTML = player[8];
            var ftp = document.createElement('td');
            ftp.setAttribute('class', 'align-middle');
            ftp.innerHTML = player[9];

            var tpm = document.createElement('td');
            tpm.setAttribute('class', 'align-middle');
            tpm.innerHTML = player[10];
            var tpa = document.createElement('td');
            tpa.setAttribute('class', 'align-middle');
            tpa.innerHTML = player[11];
            var tpp = document.createElement('td');
            tpp.setAttribute('class', 'align-middle');
            tpp.innerHTML = player[12];

            var oreb = document.createElement('td');
            oreb.setAttribute('class', 'align-middle');
            oreb.innerHTML = player[13];
            var dreb = document.createElement('td');
            dreb.setAttribute('class', 'align-middle');
            dreb.innerHTML = player[14];
            var reb = document.createElement('td');
            reb.setAttribute('class', 'align-middle');
            reb.innerHTML = player[15];

            var ast = document.createElement('td');
            ast.setAttribute('class', 'align-middle');
            ast.innerHTML = player[16];
            var stl = document.createElement('td');
            stl.setAttribute('class', 'align-middle');
            stl.innerHTML = player[17];
            var tov = document.createElement('td');
            tov.setAttribute('class', 'align-middle');
            tov.innerHTML = player[18];
            var blk = document.createElement('td');
            blk.setAttribute('class', 'align-middle');
            blk.innerHTML = player[19];
            var pf = document.createElement('td');
            pf.setAttribute('class', 'align-middle');
            pf.innerHTML = player[20];

            tr.appendChild(position);
            tr.appendChild(name);
            tr.appendChild(min);
            tr.appendChild(pt);
            tr.appendChild(fgm);
            tr.appendChild(fga);
            tr.appendChild(fgp);
            tr.appendChild(ftm);
            tr.appendChild(fta);
            tr.appendChild(ftp);
            tr.appendChild(tpm);
            tr.appendChild(tpa);
            tr.appendChild(tpp);
            tr.appendChild(oreb);
            tr.appendChild(dreb);
            tr.appendChild(reb);
            tr.appendChild(ast);
            tr.appendChild(stl);
            tr.appendChild(tov);
            tr.appendChild(blk);
            tr.appendChild(pf);
            playersTable.appendChild(tr);
        }
    }
}
buttons[1].onclick = function() {
    if (!(buttons[1].className === 'flip btn btn-lg btn-primary')) {
        buttons[1].setAttribute('class', 'flip btn btn-lg btn-primary');
        buttons[0].setAttribute('class', 'flip btn btn-lg border-dark');
        var playersTable = document.getElementById('playersTable');
        while (playersTable.firstChild) {
          playersTable.removeChild(playersTable.firstChild);
        }
        var circles = document.getElementsByTagName('circle');
        circles[1].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(allData[2][16])) / 100 + "px");
        circles[3].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(allData[2][19])) / 100 + "px");
        circles[5].setAttribute('stroke-dashoffset', '339.292' * (100 - Number(allData[2][22])) / 100 + "px");

        var inner = document.getElementsByClassName('inner');
        inner[0].innerHTML = allData[2][14] + "/" + allData[2][15];
        inner[1].innerHTML = allData[2][16] + "%";
        inner[2].innerHTML = allData[2][17] + "/" + allData[2][18];
        inner[3].innerHTML = allData[2][19] + "%";
        inner[4].innerHTML = allData[2][20] + "/" + allData[2][21];
        inner[5].innerHTML = allData[2][22] + "%";
        for (var i = 0; i < allData[2][allData[2].length - 1].length; i++) {
            player = allData[2][allData[2].length - 1][i];
            var tr = document.createElement('tr');
            var position = document.createElement('td');
            position.setAttribute('scope', 'row');
            position.setAttribute('class', 'align-middle');
            position.innerHTML = player[2];
            var name = document.createElement('td');
            name.setAttribute('class', 'align-middle text-left');
            name.innerHTML = player[0];
            var min = document.createElement('td');
            min.setAttribute('class', 'align-middle');
            min.innerHTML = player[3];
            var pt = document.createElement('td');
            pt.setAttribute('class', 'align-middle');
            pt.innerHTML = player[1];

            var fgm = document.createElement('td');
            fgm.setAttribute('class', 'align-middle');
            fgm.innerHTML = player[4];
            var fga = document.createElement('td');
            fga.setAttribute('class', 'align-middle');
            fga.innerHTML = player[5];
            var fgp = document.createElement('td');
            fgp.setAttribute('class', 'align-middle');
            fgp.innerHTML = player[6];

            var ftm = document.createElement('td');
            ftm.setAttribute('class', 'align-middle');
            ftm.innerHTML = player[7];
            var fta = document.createElement('td');
            fta.setAttribute('class', 'align-middle');
            fta.innerHTML = player[8];
            var ftp = document.createElement('td');
            ftp.setAttribute('class', 'align-middle');
            ftp.innerHTML = player[9];

            var tpm = document.createElement('td');
            tpm.setAttribute('class', 'align-middle');
            tpm.innerHTML = player[10];
            var tpa = document.createElement('td');
            tpa.setAttribute('class', 'align-middle');
            tpa.innerHTML = player[11];
            var tpp = document.createElement('td');
            tpp.setAttribute('class', 'align-middle');
            tpp.innerHTML = player[12];

            var oreb = document.createElement('td');
            oreb.setAttribute('class', 'align-middle');
            oreb.innerHTML = player[13];
            var dreb = document.createElement('td');
            dreb.setAttribute('class', 'align-middle');
            dreb.innerHTML = player[14];
            var reb = document.createElement('td');
            reb.setAttribute('class', 'align-middle');
            reb.innerHTML = player[15];

            var ast = document.createElement('td');
            ast.setAttribute('class', 'align-middle');
            ast.innerHTML = player[16];
            var stl = document.createElement('td');
            stl.setAttribute('class', 'align-middle');
            stl.innerHTML = player[17];
            var tov = document.createElement('td');
            tov.setAttribute('class', 'align-middle');
            tov.innerHTML = player[18];
            var blk = document.createElement('td');
            blk.setAttribute('class', 'align-middle');
            blk.innerHTML = player[19];
            var pf = document.createElement('td');
            pf.setAttribute('class', 'align-middle');
            pf.innerHTML = player[20];

            tr.appendChild(position);
            tr.appendChild(name);
            tr.appendChild(min);
            tr.appendChild(pt);
            tr.appendChild(fgm);
            tr.appendChild(fga);
            tr.appendChild(fgp);
            tr.appendChild(ftm);
            tr.appendChild(fta);
            tr.appendChild(ftp);
            tr.appendChild(tpm);
            tr.appendChild(tpa);
            tr.appendChild(tpp);
            tr.appendChild(oreb);
            tr.appendChild(dreb);
            tr.appendChild(reb);
            tr.appendChild(ast);
            tr.appendChild(stl);
            tr.appendChild(tov);
            tr.appendChild(blk);
            tr.appendChild(pf);
            playersTable.appendChild(tr);
        }
    }
}

var cards = document.getElementsByClassName('card');
cards[0].onclick = function() {
    var body = document.getElementsByClassName('modal-body')[0];
    while (body.firstChild) {
      body.removeChild(body.firstChild);
    }
    if (recap[0] == "Error") {
      var h1 = document.createElement("h1");
      h1.innerHTML = "No Article :(";
      body.appendChild(h1);
    } else {      
      var h1 = document.createElement("h1");
      h1.innerHTML = recap[0];
      body.appendChild(h1);
      for (var j = 2; j < recap.length; j++) {
        var p = document.createElement("p");
        p.innerHTML = recap[j];
        body.appendChild(p);
      }
    }
    $('#myModal').modal('show');
}