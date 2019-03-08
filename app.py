import os
import json
import http.client
import urllib.request
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

teams = {
    "Cleveland Cavaliers": ["static/images/logos/cavs.png", "/static/images/mini_logos/cavs.png"],
    "Detroit Pistons": ["static/images/logos/pistons.png", "/static/images/mini_logos/pistons.png"],
    "Indiana Pacers": ["static/images/logos/pacers.gif", "/static/images/mini_logos/pacers.png"],
    "Orlando Magic": ["static/images/logos/magic.gif", "/static/images/mini_logos/magic.png"],
    "Miami Heat": ["static/images/logos/heat.gif", "/static/images/mini_logos/heat.png"],
    "Brooklyn Nets": ["static/images/logos/nets.png", "/static/images/mini_logos/nets.png"],
    "Philadelphia 76ers": ["static/images/logos/sixers.png", "/static/images/mini_logos/sixers.png"],
    "Golden State Warriors": ["static/images/logos/warriors.gif", "/static/images/mini_logos/warriors.png"],
    "Dallas Mavericks": ["static/images/logos/mavs.png", "/static/images/mini_logos/mavs.png"],
    "Memphis Grizzlies": ["static/images/logos/grizzlies.png", "/static/images/mini_logos/grizzlies.png"],
    "San Antonio Spurs": ["static/images/logos/spurs.gif", "/static/images/mini_logos/spurs.png"],
    "Oklahoma City Thunder": ["static/images/logos/thunder.gif", "/static/images/mini_logos/thunder.png"],
    "Utah Jazz": ["static/images/logos/jazz.png", "/static/images/mini_logos/jazz.png"],
    "Milwaukee Bucks": ["static/images/logos/bucks.png", "/static/images/mini_logos/bucks.png"],
    "Phoenix Suns": ["static/images/logos/suns.png", "/static/images/mini_logos/suns.png"],
    "Los Angeles Lakers": ["static/images/logos/lakers.png", "/static/images/mini_logos/lakers.png"],
    "Denver Nuggets": ["static/images/logos/nuggets.png", "/static/images/mini_logos/nuggets.png"],
    "New Orleans Pelicans": ["static/images/logos/pelicans.png", "/static/images/mini_logos/pelicans.png"],
    "Sacramento Kings": ["static/images/logos/kings.png", "/static/images/mini_logos/kings.png"],
    "Los Angeles Clippers": ["static/images/logos/clippers.png", "/static/images/mini_logos/clippers.png"],
    "Chicago Bulls": ["static/images/logos/bulls.png", "/static/images/mini_logos/bulls.png"],
    "Portland Trail Blazers": ["static/images/logos/blazers.gif", "/static/images/mini_logos/blazers.png"],
    "Boston Celtics": ["static/images/logos/celtics.png", "/static/images/mini_logos/celtics.png"],
    "Minnesota Timberwolves": ["static/images/logos/wolves.png", "/static/images/mini_logos/wolves.png"],
    "Atlanta Hawks": ["static/images/logos/hawks.png", "/static/images/mini_logos/hawks.png"],
    "Washington Wizards": ["static/images/logos/wizards.png", "/static/images/mini_logos/wizards.png"],
    "Houston Rockets": ["static/images/logos/rockets.gif", "/static/images/mini_logos/rockets.png"],
    "Charlotte Hornets": ["static/images/logos/hornets.png", "/static/images/mini_logos/hornets.png"],
    "Toronto Raptors": ["static/images/logos/raptors.png", "/static/images/mini_logos/raptors.png"],
    "New York Knicks": ["static/images/logos/knicks.gif", "/static/images/mini_logos/knicks.png"]
}

def getTime(time):
    day = list(str(time))
    day = day[0:19]
    del day[10]
    day.insert(10, "T")
    day = ''.join(day)
    day += "+00:00"
    currentTime = datetime.fromisoformat(day).timestamp()
    return currentTime

def openStore(currentTime):
    upcoming = []
    file = open("static/database/store.txt", "r")
    N = int(file.readline().strip("\n"))
    for i in range(N):
        info = []
        gameTime = float(file.readline().strip("\n"))
        if gameTime > currentTime:
            info.append(gameTime)
            file.readline()
            d1 = str(date.fromtimestamp(gameTime))
            d2 = str(date.fromtimestamp(currentTime))
            n1 = int(d1[0:4]) * 365 + int(d1[5:7]) * 30 + int(d1[8:10])
            n2 = int(d2[0:4]) * 365 + int(d2[5:7]) * 30 + int(d2[8:10])
            if n1 == n2:
                info.append("Today")
            elif n1 - n2 == 1:
                info.append("Tomorrow")
            else:
                dayMapping = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
                dayOfWeek = dayMapping[date(int(d1[0:4]), int(d1[5:7]), int(d1[8:10])).weekday()]
                string = dayOfWeek + ", " + str(int(d1[5:7])) + "/" + str(int(d1[8:10]))
                info.append(string)
            for j in range(5):
                info.append(file.readline().strip("\n"))
            upcoming.append(info)
        else:
            for i in range(6):
                file.readline()
    file.close()
    return upcoming

def openDate():
    file = open("static/database/date.txt", "r")
    a = file.readline().strip("\n")
    b = file.readline().strip("\n")
    c = file.readline().strip("\n")
    file.close()
    return a, b, c

def writeXML(year, month, day):
    if year % 400 == 0:
        leap_year = True
    elif year % 100 == 0:
        leap_year = False
    elif year % 4 == 0:
        leap_year = True
    else:
        leap_year = False
    if month in (1, 3, 5, 7, 8, 10, 12):
        month_length = 31
    elif month == 2:
        if leap_year:
            month_length = 29
        else:
            month_length = 28
    else:
        month_length = 30
    if day < month_length:
        day += 1
    else:
        day = 1
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    conn = http.client.HTTPSConnection("api.sportradar.us")
    conn.request("GET", "/nba/trial/v5/en/games/" + str(year) + "/" + str(month) + "/" + str(day) + "/schedule.xml?api_key=rafgw5sffp5tj5g437uhc7we")
    res = conn.getresponse()
    data = res.read()
    text = data.decode("utf-8")
    file = open("static/xml/upcoming/upcoming_" + str(year) + "_" + str(month) + "_" + str(day) + ".xml", "w")
    file.write(text)
    file.close()
    return str(year), str(month), str(day)

def changeStore(upcoming):
    file = open("static/database/store.txt", "w")
    file.write(str(len(upcoming)) + "\n")
    for i in range(len(upcoming)):
        for j in upcoming[i]:
            file.write(str(j) + "\n")
    file.close()
    return ''

def changeDate(currentTime):
    num = str(date.fromtimestamp(currentTime))
    a = str(int(num[0:4]))
    b = str(int(num[5:7]))
    c = str(int(num[8:10]))
    file = open("static/database/date.txt", "w")
    file.write(a + "\n")
    file.write(b + "\n")
    file.write(c + "\n")
    file.close()
    return ''

def updateUpcoming(upcoming, currentTime, offset, a, b, c):
    overlap = False
    while len(upcoming) < 6:
        a, b, c = writeXML(int(a), int(b), int(c))
        tree = ET.parse("static/xml/upcoming/upcoming_" + a + "_" + b + "_" + c + ".xml")
        info = []
        for elem in tree.iter():
            if elem.tag == "{http://feed.elasticstats.com/schema/basketball/schedule-v5.0.xsd}game":
                if elem.attrib["status"] == "closed":
                    os.remove("static/xml/upcoming/upcoming_" + a + "_" + b + "_" + c + ".xml")
                    writeXML(int(a), int(b), int(c))
                    break
                
                time = elem.attrib["scheduled"]
                gameTime = datetime.fromisoformat(time).timestamp() - offset
                d1 = str(date.fromtimestamp(gameTime))
                d2 = str(date.fromtimestamp(currentTime))
                if gameTime > currentTime:
                    info.append(gameTime)
                    n1 = int(d1[0:4]) * 365 + int(d1[5:7]) * 30 + int(d1[8:10])
                    n2 = int(d2[0:4]) * 365 + int(d2[5:7]) * 30 + int(d2[8:10])
                    if n1 == n2:
                        info.append("Today")
                    elif n1 - n2 == 1:
                        info.append("Tomorrow")
                    else:
                        dayMapping = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
                        dayOfWeek = dayMapping[date(int(d1[0:4]), int(d1[5:7]), int(d1[8:10])).weekday()]
                        string = dayOfWeek + ", " + str(int(d1[5:7])) + "/" + str(int(d1[8:10]))
                        info.append(string)
                    h = int(time[11:13]) - offset // 3600
                    m = time[14:16]
                    if h < 0:
                        h += 24
                    if h == 0:
                        h += 12
                        info.append(str(h) + ":" + m + " AM")
                        continue
                    if h > 12:
                        h -= 12
                        info.append(str(h) + ":" + m + " PM")
                    elif h == 12:
                        info.append(str(h) + ":" + m + " PM")
                    else:
                        info.append(str(h) + ":" + m + " AM")
                else:
                    overlap = True
            elif elem.tag == "{http://feed.elasticstats.com/schema/basketball/schedule-v5.0.xsd}home" or elem.tag == "{http://feed.elasticstats.com/schema/basketball/schedule-v5.0.xsd}away":
                if overlap == False:
                    info.append(elem.attrib["name"])
                    info.append(teams[elem.attrib["name"]][0])
            elif elem.tag == "{http://feed.elasticstats.com/schema/basketball/schedule-v5.0.xsd}broadcasts":
                if overlap == False:
                    upcoming.append(info)
                info = []
                overlap = False
    changeStore(upcoming)
    changeDate(currentTime)
    return upcoming

@app.route("/")
def output():
    return render_template("/index.html")

@app.route("/update", methods = ["POST"])
def update():
    players, javascript = getPlayers()
    info = request.get_json()
    offset = int(info[0])
    currentTime = getTime(info[1])
    upcoming = openStore(currentTime)
    a, b, c = openDate()
    upcoming = updateUpcoming(upcoming, currentTime, offset, a, b, c)
    upcoming.append(javascript)
    return jsonify(upcoming)

def getStandings():
    standings = []
    teamMapping = {'1610612749': "Milwaukee Bucks",
    '1610612761': "Toronto Raptors",
    '1610612754': "Indiana Pacers",
    '1610612755': "Philadelphia 76ers",
    '1610612738': "Boston Celtics",
    '1610612765': "Detroit Pistons",
    '1610612751': "Brooklyn Nets",
    '1610612766': "Charlotte Hornets",
    '1610612748': "Miami Heat",
    '1610612753': "Orlando Magic",
    '1610612764': "Washington Wizards",
    '1610612737': "Atlanta Hawks",
    '1610612741': "Chicago Bulls",
    '1610612739': "Cleveland Cavaliers",
    '1610612752': "New York Knicks",
    '1610612744': "Golden State Warriors",
    '1610612743': "Denver Nuggets",
    '1610612745': "Houston Rockets",
    '1610612760': "Oklahoma City Thunder",
    '1610612757': "Portland Trail Blazers",
    '1610612762': "Utah Jazz",
    '1610612746': "Los Angeles Clippers",
    '1610612759': "San Antonio Spurs",
    '1610612758': "Sacramento Kings",
    '1610612750': "Minnesota Timberwolves",
    '1610612747': "Los Angeles Lakers",
    '1610612740': "New Orleans Pelicans",
    '1610612742': "Dallas Mavericks",
    '1610612763': "Memphis Grizzlies",
    '1610612756': "Phoenix Suns"}
    with urllib.request.urlopen("http://data.nba.net/prod/v1/current/standings_conference.json") as url:
        data = json.loads(url.read().decode())
        east = data['league']['standard']['conference']['east']
        west = data['league']['standard']['conference']['west']
        for i in east:
            teamName = teamMapping[i['teamId']]
            logo = teams[teamName][1]
            win = i['win'] 
            loss = i['loss']
            winPct = i['winPct']
            gamesBehind = str(float(i['gamesBehind']))
            if gamesBehind == "0.0":
                gamesBehind = "-"
            conference = i['confWin'] + "-" + i['confLoss']
            home = i['homeWin'] + "-" + i['homeLoss']
            away = i['awayWin'] + "-" + i['awayLoss']
            lastTen = i['lastTenWin'] + "-" + i['lastTenLoss']
            if i['isWinStreak']:
                streak = "W" + i['streak']
            else:
                streak = "L" + i['streak']
            standings.append([logo, teamName, win, loss, winPct, gamesBehind, conference, home, away, lastTen, streak])
        for i in west:
            teamName = teamMapping[i['teamId']]
            logo = teams[teamName][1]
            win = i['win'] 
            loss = i['loss']
            winPct = i['winPct']
            gamesBehind = i['gamesBehind']
            if gamesBehind == "0":
                gamesBehind = "-"
            conference = i['confWin'] + "-" + i['confLoss']
            home = i['homeWin'] + "-" + i['homeLoss']
            away = i['awayWin'] + "-" + i['awayLoss']
            lastTen = i['lastTenWin'] + "-" + i['lastTenLoss']
            if i['isWinStreak']:
                streak = "W" + i['streak']
            else:
                streak = "L" + i['streak']
            standings.append([logo, teamName, win, loss, winPct, gamesBehind, conference, home, away, lastTen, streak])
    return standings

@app.route("/results", methods = ["POST"])
def results():
    standings = getStandings()
    return jsonify(standings)

@app.route("/standings/")
def standings():
    return render_template("/standings.html")

def getPlayers():
    file = open("static/database/players.txt", "r")
    n = int(file.readline().strip("\n"))
    players = dict()
    javascript = []
    for i in range(n):
        key = file.readline().strip("\n")
        value = file.readline().strip("\n")
        players[key] = value
        javascript.append(key)
    file.close()
    return players, javascript

def getPlayerStats(playerID):
    pass

@app.route("/playerStats/<playerName>/")
def playerStats(playerName):
    return render_template("players.html")

@app.route("/players", methods = ["POST"])
def players():
    name = request.get_json()
    players, javascript = getPlayers()
    playerID = players[name]
    return jsonify(name)

if __name__ == '__main__':
    app.run("0.0.0.0", "16")