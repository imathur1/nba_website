import os
import http.client
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, redirect, url_for

# git add .
# git commit -m ""
# git remote add origin https://github.com/imathur1/NBA_Website.git
# git push -u origin master

app = Flask(__name__)

teams = {
    "Cleveland Cavaliers": "static/images/logos/cavs.png",
    "Detroit Pistons": "static/images/logos/pistons.png",
    "Indiana Pacers": "static/images/logos/pacers.gif",
    "Orlando Magic": "static/images/logos/magic.gif",
    "Miami Heat": "static/images/logos/heat.gif",
    "Brooklyn Nets": "static/images/logos/nets.png",
    "Philadelphia 76ers": "static/images/logos/sixers.png",
    "Golden State Warriors": "static/images/logos/warriors.gif",
    "Dallas Mavericks": "static/images/logos/mavs.png",
    "Memphis Grizzlies": "static/images/logos/grizzlies.png",
    "San Antonio Spurs": "static/images/logos/spurs.gif",
    "Oklahoma City Thunder": "static/images/logos/thunder.gif",
    "Utah Jazz": "static/images/logos/jazz.png",
    "Milwaukee Bucks": "static/images/logos/bucks.png",
    "Phoenix Suns": "static/images/logos/suns.png",
    "Los Angeles Lakers": "static/images/logos/lakers.png",
    "Denver Nuggets": "static/images/logos/nuggets.png",
    "New Orleans Pelicans": "static/images/logos/pelicans.png",
    "Sacramento Kings": "static/images/logos/kings.png",
    "Los Angeles Clippers": "static/images/logos/clippers.png",
    "Chicago Bulls": "static/images/logos/bulls.png",
    "Portland Trail Blazers": "static/images/logos/blazers.gif",
    "Boston Celtics": "static/images/logos/celtics.png",
    "Minnesota Timberwolves": "static/images/logos/wolves.png",
    "Atlanta Hawks": "static/images/logos/hawks.png",
    "Washington Wizards": "static/images/logos/wizards.png",
    "Houston Rockets": "static/images/logos/rockets.gif",
    "Charlotte Hornets": "static/images/logos/hornets.png",
    "Toronto Raptors": "static/images/logos/raptors.png",
    "New York Knicks": "static/images/logos/knicks.gif"
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
    file = open("static/text/store.txt", "r")
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
    file = open("static/text/date.txt", "r")
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
    file = open("static/text/store.txt", "w")
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
    file = open("static/text/date.txt", "w")
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
                    info.append(teams[elem.attrib["name"]])
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
    return render_template("index.html")

@app.route("/update", methods = ["POST"])
def update():
    info = request.get_json()
    offset = int(info[0])
    currentTime = getTime(info[1])
    upcoming = openStore(currentTime)
    a, b, c = openDate()
    upcoming = updateUpcoming(upcoming, currentTime, offset, a, b, c)
    return jsonify(upcoming)

@app.route("/standings/")
def standings():
    return render_template("/standings.html")

if __name__ == '__main__':
    app.run("0.0.0.0", "16")