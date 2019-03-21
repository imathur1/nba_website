import os
import json
import calendar
import http.client
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
from newsapi import NewsApiClient
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

people = dict()
theDate = ""
gameID = ""
cTime = 0
name = ""
modified = ""
teams = {
    "Cleveland Cavaliers": ["http://content.sportslogos.net/logos/6/222/full/ige5q46x2v9c8hw80jhi4f85h.png", "https://ssl.gstatic.com/onebox/media/sports/logos/NAlGkmv45l1L-3NhwVhDPg_48x48.png"],
    "Detroit Pistons": ["http://content.sportslogos.net/logos/6/223/full/2164_detroit_pistons-primary-2018.png", "https://ssl.gstatic.com/onebox/media/sports/logos/qvWE2FgBX0MCqFfciFBDiw_48x48.png"],
    "Indiana Pacers": ["http://content.sportslogos.net/logos/6/224/full/gdm7egmgv3tsspc6f1gym7cwz.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/andumiE_wrpDpXvUgqCGYQ_48x48.png"],
    "Orlando Magic": ["http://content.sportslogos.net/logos/6/217/full/h2k5cbia6m8e1dbdcfxfgre84.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/p69oiJ4LDsvCJUDQ3wR9PQ_48x48.png"],
    "Miami Heat": ["http://content.sportslogos.net/logos/6/214/full/93lzfcfcnq125eh7etyxpuhfp.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/0nQXN6OF7wnLY3hJz8lZJQ_48x48.png"],
    "Brooklyn Nets": ["http://content.sportslogos.net/logos/6/3786/full/930_brooklyn-nets-partial-2013.png", "https://ssl.gstatic.com/onebox/media/sports/logos/iishUmO7vbJBE7iK2CZCdw_48x48.png"],
    "Philadelphia 76ers": ["http://content.sportslogos.net/logos/6/218/full/7034_philadelphia_76ers-primary-2016.png", "https://ssl.gstatic.com/onebox/media/sports/logos/US6KILZue2D5766trEf0Mg_48x48.png"],
    "Golden State Warriors": ["http://content.sportslogos.net/logos/6/235/full/5gzur7f6x09cv61jt16smhopl.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/XD2v321N_-vk7paF53TkAg_48x48.png"],
    "Dallas Mavericks": ["http://content.sportslogos.net/logos/6/228/full/5118_dallas_mavericks-alternate-2018.png", "https://ssl.gstatic.com/onebox/media/sports/logos/xxxlj9RpmAKJ9P9phstWCQ_48x48.png"],
    "Memphis Grizzlies": ["http://content.sportslogos.net/logos/6/231/full/7277_memphis_grizzlies-alternate-2019.png", "https://ssl.gstatic.com/onebox/media/sports/logos/3ho45P8yNw-WmQ2m4A4TIA_48x48.png"],
    "San Antonio Spurs": ["http://content.sportslogos.net/logos/6/233/full/828.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/FKwMB_85FlZ_7PTt1f7hjQ_48x48.png"],
    "Oklahoma City Thunder": ["http://content.sportslogos.net/logos/6/2687/full/qdx55wdx4akljqkvzi1s3e6t3.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/b4bJ9zKFBDykdSIGUrbWdw_48x48.png"],
    "Utah Jazz": ["http://content.sportslogos.net/logos/6/234/full/txe1ybetuoye8pirnrhqalh04.png", "https://ssl.gstatic.com/onebox/media/sports/logos/SP_dsmXEKFVZH5N1DQpZ4A_48x48.png"],
    "Milwaukee Bucks": ["http://content.sportslogos.net/logos/6/225/full/3864_milwaukee_bucks-alternate-2016.png", "https://ssl.gstatic.com/onebox/media/sports/logos/Wd6xIEIXpfqg9EZC6PAepQ_48x48.png"],
    "Phoenix Suns": ["http://content.sportslogos.net/logos/6/238/full/3834_phoenix_suns-partial-2014.png", "https://ssl.gstatic.com/onebox/media/sports/logos/pRr87i24KHWH0UuAc5EamQ_48x48.png"],
    "Los Angeles Lakers": ["http://content.sportslogos.net/logos/6/237/full/uig7aiht8jnpl1szbi57zzlsh.png", "https://ssl.gstatic.com/onebox/media/sports/logos/4ndR-n-gall7_h3f7NYcpQ_48x48.png"],
    "Denver Nuggets": ["http://content.sportslogos.net/logos/6/229/full/8954_denver_nuggets-alternate-2019.png", "https://ssl.gstatic.com/onebox/media/sports/logos/9wPFTOxV_zP1KmRRggJNqQ_48x48.png"],
    "New Orleans Pelicans": ["http://content.sportslogos.net/logos/6/4962/full/2681_new_orleans_pelicans-primary-2014.png", "https://ssl.gstatic.com/onebox/media/sports/logos/JCQO978-AWbg00TQUNPUVg_48x48.png"],
    "Sacramento Kings": ["http://content.sportslogos.net/logos/6/240/full/4043_sacramento_kings-primary-2017.png", "https://ssl.gstatic.com/onebox/media/sports/logos/wkCDHakxEThLGoZ4Ven48Q_48x48.png"],
    "Los Angeles Clippers": ["http://content.sportslogos.net/logos/6/236/full/1038_los_angeles_clippers-secondary-2016.png", "https://ssl.gstatic.com/onebox/media/sports/logos/F36nQLCQ2FND3za-Eteeqg_48x48.png"],
    "Chicago Bulls": ["http://content.sportslogos.net/logos/6/221/full/zdrycpc7mh5teihl10gko8sgf.png", "https://ssl.gstatic.com/onebox/media/sports/logos/ofjScRGiytT__Flak2j4dg_48x48.png"],
    "Portland Trail Blazers": ["http://content.sportslogos.net/logos/6/239/full/826.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/_bgagBCd6ieOIt3INWRN_w_48x48.png"],
    "Boston Celtics": ["http://content.sportslogos.net/logos/6/213/full/slhg02hbef3j1ov4lsnwyol5o.png", "https://ssl.gstatic.com/onebox/media/sports/logos/GDJBo7eEF8EO5-kDHVpdqw_48x48.png"],
    "Minnesota Timberwolves": ["http://content.sportslogos.net/logos/6/232/full/9669_minnesota_timberwolves-primary-2018.png", "https://ssl.gstatic.com/onebox/media/sports/logos/JzePt6Fp_HJMNEz-1B99yw_48x48.png"],
    "Atlanta Hawks": ["http://content.sportslogos.net/logos/6/220/full/8452_atlanta_hawks-alternate-2016.png", "https://ssl.gstatic.com/onebox/media/sports/logos/pm5l5mtY1elOQAl9ZEcm2A_48x48.png"],
    "Washington Wizards": ["http://content.sportslogos.net/logos/6/219/full/3g5wchibh2ltoh617fcpgmfio.png", "https://ssl.gstatic.com/onebox/media/sports/logos/NBkMJapxft4V5kvufec4Jg_48x48.png"],
    "Houston Rockets": ["http://content.sportslogos.net/logos/6/230/full/etpzlhc48xgh58agjuln2khsl.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/zhO6MIB1UzZmtXLHkJQBmg_48x48.png"],
    "Charlotte Hornets": ["http://content.sportslogos.net/logos/6/5120/full/1926_charlotte__hornets_-primary-2015.png", "https://ssl.gstatic.com/onebox/media/sports/logos/ToeKy5-TrHAnTCl-qhuuHQ_48x48.png"],
    "Toronto Raptors": ["http://content.sportslogos.net/logos/6/227/full/4578_toronto_raptors-primary-2016.png", "https://ssl.gstatic.com/onebox/media/sports/logos/745IgW4NSvnRxg-W9oczmQ_48x48.png"],
    "New York Knicks": ["http://content.sportslogos.net/logos/6/216/full/2nn48xofg0hms8k326cqdmuis.gif", "https://ssl.gstatic.com/onebox/media/sports/logos/-rf7eY39l_0V7J4ekakuKA_48x48.png"]
}
teamMapping = {
    '1610612749': "Milwaukee Bucks",
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
    '1610612756': "Phoenix Suns"
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
    file = open("static/xml/upcoming_" + str(year) + "_" + str(month) + "_" + str(day) + ".xml", "w")
    file.write(text)
    file.close()
    return str(year), str(month), str(day)

def deleteXML(year, month, day):
    value = 365 * year + 30 * month + day
    files = os.listdir("static/xml/")
    for i in files:
        s = i.split("_")
        y = int(s[1])
        m = int(s[2])
        d = int(s[3][:-4])
        newValue = 365 * y + 30 * m + d
        if newValue < value:
            os.remove("static/xml/" + i)

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
    count = 0
    while len(upcoming) < 6:
        count += 1
        if count >= 21:
            upcoming = "Season Over"
            break
        a, b, c = writeXML(int(a), int(b), int(c))
        deleteXML(int(a), int(b), int(c))
        tree = ET.parse("static/xml/upcoming_" + a + "_" + b + "_" + c + ".xml")
        info = []
        dates = []
        for elem in tree.iter():
            if elem.tag == "{http://feed.elasticstats.com/schema/basketball/schedule-v5.0.xsd}game":
                if elem.attrib["status"] == "closed":
                    pass
                
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
                    if info not in upcoming:
                        upcoming.append(info)
                info = []
                overlap = False
    changeStore(upcoming)
    changeDate(currentTime)
    return upcoming

def getStandings():
    standings = []
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

def getPlayers():
    global people
    players = dict()
    javascript = []
    file = open("static/database/players.txt", "r")
    year = int(file.readline().strip("\n"))
    n = int(file.readline().strip("\n"))
    for i in range(n):
        key = file.readline().strip("\n")
        value = file.readline().strip("\n")
        season = file.readline().strip("\n")
        players[key] = [value, season]
        javascript.append(key)
    file.close()

    temp = year
    while True:
        try:
            with urllib.request.urlopen("http://data.nba.net/prod/v1/" + str(year) + "/players.json") as url:
                data = json.loads(url.read().decode())
                for i in data['league']['standard']:
                    key = i['firstName'] + " " + i['lastName']
                    value = i['personId']
                    season = year
                    if key not in javascript:
                        javascript.append(key)
                    players[key] = [value, season]
            year += 1
        except urllib.error.HTTPError:
            if temp != year:
                file = open("static/database/players.txt", "w")
                file.write(str(year) + "\n")
                file.write(str(len(players)) + "\n")
                for i in players:
                    file.write(i + "\n")
                    file.write(players[i][0] + "\n")
                    file.write(str(players[i][1]) + "\n")
                file.close()
            break
    people = players
    return players, javascript

def getStats(playerID, year):
    stats = []
    try:
        with urllib.request.urlopen("http://data.nba.net/prod/v1/" + year + "/players/" + playerID + "_profile.json") as url:
            data = json.loads(url.read().decode())  
            for i in data['league']['standard']['stats']['regularSeason']['season']:
                for j in i['teams']:
                    team = teamMapping[j['teamId']]
                    logo = teams[team][1]
                    try:
                        points = float(j['ppg'])
                    except:
                        points = -1
                    try:
                        rebounds = float(j['rpg'])
                    except:
                        rebounds = -1
                    try:
                        assists = float(j['apg'])
                    except:
                        assists = -1
                    try:
                        minutes = float(j['mpg'])
                    except:
                        minutes = -1
                    try:
                        steals = float(j['spg'])
                    except:
                        steals = -1
                    try:
                        turnovers = float(j['topg'])
                    except:
                        turnovers = -1
                    try:
                        blocks = float(j['bpg'])
                    except:
                        blocks = -1
                    try:
                        totAssists = int(j['assists'])
                    except:
                        totAssists = -1
                    try:
                        totBlocks = int(j['blocks'])
                    except:
                        totBlocks = -1
                    try:
                        totSteals = int(j['steals'])
                    except:
                        totSteals = -1
                    try:
                        totTurnovers = int(j['turnovers'])
                    except:
                        totTurnovers = -1
                    try:
                        totReb = int(j['totReb'])
                    except:  
                        totReb = -1
                    try:
                        fieldGoalsMade = int(j['fgm'])
                    except:
                        fieldGoalsMade = -1
                    try:
                        fieldGoalsAttempted = int(j['fga'])
                    except:
                        fieldGoalsAttempted = -1
                    try:
                        fieldGoalPercent = float(j['fgp'])
                    except:
                        fieldGoalPercent = -1
                    try:
                        threePointsMade = int(j['tpm'])
                    except:  
                        threePointsMade = -1
                    try:
                        threePointsAttempted = int(j['tpa'])
                    except:
                        threePointsAttempted = -1
                    try:
                        threePointPercent = float(j['tpp'])
                    except:
                        threePointPercent = -1
                    try:
                        freeThrowsMade = int(j['ftm'])
                    except:
                        freeThrowsMade = -1
                    try:
                        freeThrowsAttempted = int(j['fta'])
                    except:
                        freeThrowsAttempted = -1
                    try:
                        freeThrowPercent = float(j['ftp'])
                    except:
                        freeThrowPercent = -1
                    try:
                        personalFouls = int(j['pFouls'])
                    except:
                        personalFouls = -1               
                    try:
                        totPoints = int(j['points'])
                    except:
                        totPoints = -1
                    try:
                        gamesPlayed = int(j['gamesPlayed'])
                    except:
                        gamesPlayed = -1
                    try:
                        gamesStarted = int(j['gamesStarted'])
                    except:
                        gamesStarted = -1
                    try:
                        totMinutes = int(j['min'])
                    except:
                        totMinutes = -1
                    try:
                        doubleDoubles = int(j['dd2'])
                    except:
                        doubleDoubles = -1
                    try:
                        tripleDoubles = int(j['td3'])
                    except:
                        tripleDoubles = -1
                    stats.append([i['seasonYear'], logo, team, totMinutes, minutes, totPoints, points, 
                    totAssists, assists, totReb, rebounds, totBlocks, blocks, totSteals, steals,
                    totTurnovers, turnovers, threePointsMade, threePointsAttempted, threePointPercent,
                    fieldGoalsMade, fieldGoalsAttempted, fieldGoalPercent, freeThrowsMade,
                    freeThrowsAttempted, freeThrowPercent, personalFouls, gamesPlayed, gamesStarted,
                    doubleDoubles, tripleDoubles])
                    
            try:
                career = data['league']['standard']['stats']['careerSummary']
                logo = ""
                team = ""
                points = float(career['ppg'])
                rebounds = float(career['rpg'])
                assists = float(career['apg'])
                minutes = float(career['mpg'])
                steals = float(career['spg'])
                blocks = float(career['bpg'])
                totAssists = int(career['assists'])
                totBlocks = int(career['blocks'])
                totSteals = int(career['steals'])
                totTurnovers = int(career['turnovers'])
                totReb = int(career['totReb'])
                fieldGoalsMade = int(career['fgm'])
                fieldGoalsAttempted = int(career['fga'])
                fieldGoalPercent = float(career['fgp'])
                threePointsMade = int(career['tpm'])
                threePointsAttempted = int(career['tpa'])
                threePointPercent = float(career['tpp'])
                freeThrowsMade = int(career['ftm'])
                freeThrowsAttempted = int(career['fta'])
                freeThrowPercent = float(career['ftp'])
                personalFouls = int(career['pFouls'])
                totPoints = int(career['points'])
                gamesPlayed = int(career['gamesPlayed'])
                gamesStarted = int(career['gamesStarted'])
                totMinutes = int(career['min'])
                doubleDoubles = int(career['dd2'])
                tripleDoubles = int(career['td3'])

                stats.append(["Career", logo, team, totMinutes, minutes, totPoints, points, 
                totAssists, assists, totReb, rebounds, totBlocks, blocks, totSteals, steals,
                totTurnovers, "None", threePointsMade, threePointsAttempted, threePointPercent,
                fieldGoalsMade, fieldGoalsAttempted, fieldGoalPercent, freeThrowsMade,
                freeThrowsAttempted, freeThrowPercent, personalFouls, gamesPlayed, gamesStarted,
                doubleDoubles, tripleDoubles])
            except:
                stats.append(["Career", -1, -1, -1])

        background = []
        n = name.split(" ")
        with urllib.request.urlopen("https://www.nba.com/players/" + n[0].lower() + "/" + n[1].lower() + "/" + playerID) as url:
            data = url.read().decode()
            parsed = BeautifulSoup(data, features='lxml')
            try:
                jersey = parsed.body.find('span', attrs={'class':'nba-player-header__jersey-number'}).text
            except AttributeError:
                jersey = "None"
            try:
                position = parsed.body.find('span', attrs={'class':'nba-player-header__position'}).text
            except AttributeError:
                position = "None"
            try:
                height = parsed.body.findAll('p', attrs={'class':'nba-player-vitals__top-info-imperial'})
            except AttributeError:
                height = "None"

            try:
                children1 = height[0].findChildren("span", recursive=False)
                height1 = children1[0].text + " " + children1[1].text
            except:
                height1 = "None"
            try:
                children2 = height[1].findChildren("span", recursive=False)
                weight1 = children2[0].text
            except:
                weight1 = "None"
            
            try:
                info = parsed.body.findAll('span', attrs={'class':'nba-player-vitals__bottom-info'})
                born = info[0].text.strip()
                age = info[1].text.strip()
                from1 = info[2].text.strip()
                debut = info[3].text.strip()
                years = info[4].text.strip()
            except:
                info = "None"
                born = "None"
                age = "None"
                from1 = "None"
                debut = "None"
                years = "None"
            image = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + playerID + ".png"
            background = [jersey, position, height1, weight1, born, age, from1, debut, years, image]

        stats.append(background)
    except urllib.error.HTTPError:
        return "Error"
    return stats

def getPreviewArticles(upcoming):
    preview = []
    articleInfo = []
    for i in range(6):
        d = str(date.fromtimestamp(upcoming[i][0])).replace("-", "")
        teams = [upcoming[i][3], upcoming[i][5]]
        with urllib.request.urlopen("http://data.nba.net/prod/v2/" + d + "/scoreboard.json") as url:
            data = json.loads(url.read().decode()) 
            for i in data['games']:
                game = i['gameId']
                t1 = teamMapping[i['vTeam']['teamId']]
                t2 = teamMapping[i['hTeam']['teamId']]
                if t1 in teams and t2 in teams:
                    try:
                        with urllib.request.urlopen("http://data.nba.net/prod/v1/" + d + "/" + game + "_preview_article.json") as url:
                            data2 = json.loads(url.read().decode()) 
                            title = data2['title']
                            copyright = data2['copyright']
                            info = [title, copyright]
                            for i in data2['paragraphs']:
                                info.append(i['paragraph'])
                        articleInfo.append(info)
                    except urllib.error.HTTPError:
                        articleInfo.append("Error")

    return articleInfo

def getNews(date1, date2):
    newsapi = NewsApiClient(api_key='7477d1d0e72844348ebc6472a323c125')
    top_headlines = newsapi.get_top_headlines(q='nba',
                                            category='sports',
                                            language='en',
                                            country='us')
    all_articles = newsapi.get_everything(q='nba',
                                        sources='espn,bleacher-report',
                                        domains='espn.com,bleacherreport.com,nba.com',
                                        from_param=date1,
                                        to=date2,
                                        language='en',
                                        sort_by='relevancy')

    seen = []
    data = []
    articles1 = top_headlines['articles']
    articles2 = all_articles['articles']
    data.append(len(articles1))
    for i in articles1:
        source = i['source']['name']
        author = i['author']
        title = i['title']
        url = i['url']
        image = i['urlToImage']
        time = i['publishedAt']
        content = i['content']
        if source == 'Espn.com' or source == 'Nba.com' or source == 'Bleacher Report':
            if title not in seen:
                seen.append(title)
                by = ""
                if author is None:
                    by = source
                elif author == "NBA.com":
                    author = "Official release"
                    by = author + " from " + source
                else:
                    by = author + " from " + source
                if content is None:
                    content = "No content"
                if image is None:
                    image = "https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwin0ffp8v3gAhUcoYMKHaydCjYQjRx6BAgBEAU&url=https%3A%2F%2Fwww.apple.com%2Fshop%2Frefurbished%2Fclearance&psig=AOvVaw1B-rVuUmLBsRLXeO_bHC2o&ust=1552524562379261"
                
                mapping = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May",
                "06":"June", "07": "July", "08": "August","09": "September", "10": "October",
                "11":"November", "12":"December"}
                time = mapping[time[5:7]] + " " + str(int(time[8:10])) + ", " + time[0:4]
                content = content.replace('\xa0', ' -')
                data.append([title, by, time, content, image, url])

    for i in articles2:
        source = i['source']['name']
        author = i['author']
        title = i['title']
        url = i['url']
        image = i['urlToImage']
        time = i['publishedAt']
        content = i['content']
        if title not in seen:
            seen.append(title)
            by = ""
            if author is None:
                by = source
            elif author == "NBA.com":
                author = "Official release"
                by = author + " from " + source
            else:
                by = author + " from " + source
            if content is None:
                content = "No content"
            if image is None:
                image = "https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwin0ffp8v3gAhUcoYMKHaydCjYQjRx6BAgBEAU&url=https%3A%2F%2Fwww.apple.com%2Fshop%2Frefurbished%2Fclearance&psig=AOvVaw1B-rVuUmLBsRLXeO_bHC2o&ust=1552524562379261"
            
            mapping = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May",
            "06":"June", "07": "July", "08": "August","09": "September", "10": "October",
            "11":"November", "12":"December"}
            time = mapping[time[5:7]] + " " + str(int(time[8:10])) + ", " + time[0:4]
            content = content.replace('\xa0', '  -')
            data.append([title, by, time, content, image, url])
    return data

def updateRecent(time):
    global theDate
    userTime = getTime(time[1])
    day = 0
    recent = []
    while len(recent) < 6:
        d = str(date.fromtimestamp(userTime - 86400 * day)).replace("-", "")
        theDate = d
        with urllib.request.urlopen("http://data.nba.net/prod/v1/" + d + "/scoreboard.json") as url:
            data = json.loads(url.read().decode())
            for i in data['games']:
                if i['statusNum'] == 3:
                    gameID = i['gameId']
                    team1 = teamMapping[i['vTeam']['teamId']]
                    logo1 = teams[team1][0]
                    record1 = "(" + i['vTeam']['win'] + " - " + i['vTeam']['loss'] + ")"
                    score1 = i['vTeam']['score']
                    team2 = teamMapping[i['hTeam']['teamId']]
                    logo2 = teams[team2][0]
                    record2 = "(" + i['hTeam']['win'] + " - " + i['hTeam']['loss'] + ")"
                    score2 = i['hTeam']['score']
                    recent.append([team1, logo1, record1, score1, team2, logo2, record2, score2, gameID, d])
        day += 1
    return recent

@app.route("/")
def output():
    return render_template("/index.html")

@app.route("/update", methods = ["POST"])
def update():
    global cTime
    info = request.get_json()
    offset = int(info[0])
    currentTime = getTime(info[1])
    cTime = currentTime
    upcoming = openStore(currentTime)
    a, b, c = openDate()
    upcoming = updateUpcoming(upcoming, currentTime, offset, a, b, c)
    if upcoming == "Season Over":
        return jsonify(upcoming)
    else:
        preview = getPreviewArticles(upcoming)
        upcoming.append(preview)
        return jsonify(upcoming)

@app.route("/updateAutocomplete", methods = ["POST"])
def updateAutocomplete():
    players, javascript = getPlayers()
    return jsonify(javascript)

@app.route('/gameID', methods = ["POST"])
def game_id():
    global gameID
    global theDate
    inputs = request.get_json()
    if type(inputs) == list:
        gameID = inputs[0]
        theDate = inputs[1]
    else:
        gameID = inputs
    if type(gameID) == list:
        gameID = gameID[0]
    return ''

@app.route('/gameUpdate', methods = ["POST"])
def gameUpdate():
    recap = []
    try:
        with urllib.request.urlopen("http://data.nba.net/prod/v1/" + theDate + "/" + gameID + "_recap_article.json") as url:
            data = json.loads(url.read().decode())
            title = data['title']
            copyright = data['copyright']
            info = [title, copyright]
            for i in data['paragraphs']:
                recap.append(i['paragraph'])
    except urllib.error.HTTPError:
        recap == ["Error"]

    info = []
    try:
        with urllib.request.urlopen("http://data.nba.net/prod/v1/" + theDate + "/" + gameID + "_boxscore.json") as url:
            data = json.loads(url.read().decode())

            both = []
            arena = data['basicGameData']['arena']['name']
            city = data['basicGameData']['arena']['city']
            abbrv = data['basicGameData']['arena']['stateAbbr']
            startTime = data['basicGameData']['startTimeEastern']
            startDate = data['basicGameData']['startDateEastern']

            days = {0: "Monday, ", 1: "Tuesday, ", 2: "Wednesday, ", 3: "Thursday, ", 
            4: "Friday, ", 5: "Saturday, ", 6: "Sunday, "}
            months = {1:"January ", 2:"February ", 3:"March ", 4:"April ", 5:"May ",
            6:"June", 7: "July ", 8: "August ", 9: "September ", 10: "October ",
            11:"November ", 12:"December "}
            year = int(startDate[0:4])
            month = int(startDate[4:6])
            day = int(startDate[6:8])
            when = days[calendar.weekday(year, month, day)] + months[month] + str(day) + ", " + str(year) + " • " + startTime
            where = arena + " • " + city + ", " + abbrv
            text = data['basicGameData']['nugget']['text']
            attendance = data['basicGameData']['attendance']
            duration = int(data['basicGameData']['gameDuration']['hours']) * 60 + int(data['basicGameData']['gameDuration']['minutes'])
            
            t1 = []
            t2 = []
            team1 = teamMapping[data['basicGameData']['vTeam']['teamId']]
            logo1 = teams[team1][0]
            miniLogo1 = teams[team1][1]
            triCode1 = data['basicGameData']['vTeam']['triCode']
            record1 = "(" + data['basicGameData']['vTeam']['win'] + " - " + data['basicGameData']['vTeam']['loss'] + ")"
            score1 = data['basicGameData']['vTeam']['score']
            quarters1 = []
            for i in data['basicGameData']['vTeam']['linescore']:
                quarters1.append(i['score'])

            team2 = teamMapping[data['basicGameData']['hTeam']['teamId']]
            logo2 = teams[team2][0]
            miniLogo2 = teams[team2][1]
            triCode2 = data['basicGameData']['hTeam']['triCode']
            record2 = "(" + data['basicGameData']['hTeam']['win'] + " - " + data['basicGameData']['hTeam']['loss'] + ")"
            score2 = data['basicGameData']['hTeam']['score']
            quarters2 = []
            for i in data['basicGameData']['hTeam']['linescore']:
                quarters2.append(i['score'])

            timesTied = data['stats']['timesTied']
            leadChanges = data['stats']['leadChanges']
            both = [when, where, text, attendance, duration, timesTied, leadChanges]

            fastBreakPoints1 = data['stats']['vTeam']['fastBreakPoints']
            pointsInPaint1 = data['stats']['vTeam']['pointsInPaint']
            biggestLead1 = data['stats']['vTeam']['biggestLead']
            secondChancePoints1 = data['stats']['vTeam']['secondChancePoints']
            pointsOffTurnovers1 = data['stats']['vTeam']['pointsOffTurnovers']
            longestRun1 = data['stats']['vTeam']['longestRun']
            totalPoints1 = data['stats']['vTeam']['totals']['points']
            fieldGoalsMade1 = data['stats']['vTeam']['totals']['fgm']
            fieldGoalsAttempted1 = data['stats']['vTeam']['totals']['fga']
            fieldGoalPercentage1 = data['stats']['vTeam']['totals']['fgp']
            freeThrowsMade1 = data['stats']['vTeam']['totals']['ftm']
            freeThrowsAttempted1 = data['stats']['vTeam']['totals']['fta']
            freeThrowPercentage1 = data['stats']['vTeam']['totals']['ftp']
            threePointsMade1 = data['stats']['vTeam']['totals']['tpm']
            threePointsAttempted1 = data['stats']['vTeam']['totals']['tpa']
            threePointPercentage1 = data['stats']['vTeam']['totals']['tpp']
            offensiveRebounds1 = data['stats']['vTeam']['totals']['offReb']
            defensiveRebounds1 = data['stats']['vTeam']['totals']['defReb']
            totalRebounds1 = data['stats']['vTeam']['totals']['totReb']
            assists1 = data['stats']['vTeam']['totals']['assists']
            steals1 = data['stats']['vTeam']['totals']['steals']
            turnovers1 = data['stats']['vTeam']['totals']['turnovers']
            blocks1 = data['stats']['vTeam']['totals']['blocks']
            minutes1 = data['stats']['vTeam']['totals']['min']
            personalFouls1 = data['stats']['vTeam']['totals']['pFouls']
            pointsLeader1 = data['stats']['vTeam']['leaders']['points']['value']
            assistsLeader1 = data['stats']['vTeam']['leaders']['assists']['value']
            reboundsLeader1 = data['stats']['vTeam']['leaders']['rebounds']['value']
            t1 = [team1, logo1, miniLogo1, triCode1, record1, score1, quarters1, fastBreakPoints1, pointsInPaint1,
            biggestLead1, secondChancePoints1, pointsOffTurnovers1, longestRun1, totalPoints1,
            fieldGoalsMade1, fieldGoalsAttempted1, fieldGoalPercentage1, freeThrowsMade1,
            freeThrowsAttempted1, freeThrowPercentage1, threePointsMade1, threePointsAttempted1,
            threePointPercentage1, minutes1, offensiveRebounds1, defensiveRebounds1, totalRebounds1,
            assists1, steals1, turnovers1, blocks1, personalFouls1, pointsLeader1, assistsLeader1,
            reboundsLeader1]

            fastBreakPoints2 = data['stats']['hTeam']['fastBreakPoints']
            pointsInPaint2 = data['stats']['hTeam']['pointsInPaint']
            biggestLead2 = data['stats']['hTeam']['biggestLead']
            secondChancePoints2 = data['stats']['hTeam']['secondChancePoints']
            pointsOffTurnovers2 = data['stats']['hTeam']['pointsOffTurnovers']
            longestRun2 = data['stats']['hTeam']['longestRun']
            totalPoints2 = data['stats']['hTeam']['totals']['points']
            fieldGoalsMade2 = data['stats']['hTeam']['totals']['fgm']
            fieldGoalsAttempted2 = data['stats']['hTeam']['totals']['fga']
            fieldGoalPercentage2 = data['stats']['hTeam']['totals']['fgp']
            freeThrowsMade2 = data['stats']['hTeam']['totals']['ftm']
            freeThrowsAttempted2 = data['stats']['hTeam']['totals']['fta']
            freeThrowPercentage2 = data['stats']['hTeam']['totals']['ftp']
            threePointsMade2 = data['stats']['hTeam']['totals']['tpm']
            threePointsAttempted2 = data['stats']['hTeam']['totals']['tpa']
            threePointPercentage2 = data['stats']['hTeam']['totals']['tpp']
            offensiveRebounds2 = data['stats']['hTeam']['totals']['offReb']
            defensiveRebounds2 = data['stats']['hTeam']['totals']['defReb']
            totalRebounds2 = data['stats']['hTeam']['totals']['totReb']
            assists2 = data['stats']['hTeam']['totals']['assists']
            steals2 = data['stats']['hTeam']['totals']['steals']
            turnovers2 = data['stats']['hTeam']['totals']['turnovers']
            blocks2 = data['stats']['hTeam']['totals']['blocks']
            minutes2 = data['stats']['vTeam']['totals']['min']
            personalFouls2 = data['stats']['hTeam']['totals']['pFouls']
            pointsLeader2 = data['stats']['hTeam']['leaders']['points']['value']
            assistsLeader2 = data['stats']['hTeam']['leaders']['assists']['value']
            reboundsLeader2 = data['stats']['hTeam']['leaders']['rebounds']['value']
            t2 = [team2, logo2, miniLogo2, triCode2, record2, score2, quarters2, fastBreakPoints2, pointsInPaint2,
            biggestLead2, secondChancePoints2, pointsOffTurnovers2, longestRun2, totalPoints2,
            fieldGoalsMade2, fieldGoalsAttempted2, fieldGoalPercentage2, freeThrowsMade2,
            freeThrowsAttempted2, freeThrowPercentage2, threePointsMade2, threePointsAttempted2,
            threePointPercentage2, minutes2, offensiveRebounds2, defensiveRebounds2, totalRebounds2,
            assists2, steals2, turnovers2, blocks2, personalFouls2, pointsLeader2, assistsLeader2,
            reboundsLeader2]

            players1 = []
            players2 = []
            for i in data['stats']['activePlayers']:
                playerName = ""
                for j in people:
                    if people[j][0] == i['personId']:
                        playerName = j
                playerPoints = i['points']
                playerPosition = i['pos']
                playerMinutes = i['min']
                playerFieldGoalsMade = i['fgm']
                playerFieldGoalsAttempted = i['fga']
                playerFieldGoalPercentage = i['fgp']
                playerFreeThrowsMade = i['ftm']
                playerFreeThrowsAttempted = i['fta']
                playerFreeThrowPercentage = i['ftp']
                playerThreePointsMade = i['tpm']
                playerThreePointsAttempted = i['tpa']
                playerThreePointPercentage = i['tpp']
                playerOffensiveRebounds = i['offReb']
                playerDefensiveRebounds = i['defReb']
                playerTotalRebounds = i['totReb']
                playerAssists = i['assists']
                playerSteals = i['steals']
                playerTurnovers = i['turnovers']
                playerBlocks = i['blocks']
                playerPersonalFouls = i['pFouls']

                if i['teamId'] == data['basicGameData']['vTeam']['teamId']:
                    players1.append([playerName, playerPoints, playerPosition, playerMinutes, 
                    playerFieldGoalsMade, playerFieldGoalsAttempted, playerFieldGoalPercentage,
                    playerFreeThrowsMade, playerFreeThrowsAttempted, playerFreeThrowPercentage,
                    playerThreePointsMade, playerThreePointsAttempted, playerThreePointPercentage,
                    playerOffensiveRebounds, playerDefensiveRebounds, playerTotalRebounds,
                    playerAssists, playerSteals, playerTurnovers, playerBlocks, playerPersonalFouls])
                else:
                    players2.append([playerName, playerPoints, playerPosition, playerMinutes, 
                    playerFieldGoalsMade, playerFieldGoalsAttempted, playerFieldGoalPercentage,
                    playerFreeThrowsMade, playerFreeThrowsAttempted, playerFreeThrowPercentage,
                    playerThreePointsMade, playerThreePointsAttempted, playerThreePointPercentage,
                    playerOffensiveRebounds, playerDefensiveRebounds, playerTotalRebounds,
                    playerAssists, playerSteals, playerTurnovers, playerBlocks, playerPersonalFouls])
            
            t1.append(players1)
            t2.append(players2)
            info = [both, t1, t2, recap]

    except urllib.error.HTTPError:
        info = "NO DATA"
    return jsonify(info)

@app.route('/scores/<gameID>/')
def gameInfo(gameID):
    return render_template("gameInfo.html")

@app.route('/recent', methods = ["POST"])
def recent():
    time = request.get_json()
    recent = updateRecent(time)
    return jsonify(recent)

@app.route("/gameDate", methods = ["POST"])
def gameDate():
    global theDate
    date = request.get_json()
    theDate = date
    info = []
    try:
        with urllib.request.urlopen("http://data.nba.net/prod/v1/" + date + "/scoreboard.json") as url:
            data = json.loads(url.read().decode())
            if data['numGames'] == 0:
                info = "NO GAMES"
            else:
                for i in data['games']:
                    if i['statusNum'] == 3:
                        gameID = i['gameId']
                        team1 = teamMapping[i['vTeam']['teamId']]
                        logo1 = teams[team1][0]
                        record1 = "(" + i['vTeam']['win'] + " - " + i['vTeam']['loss'] + ")"
                        score1 = i['vTeam']['score']
                        team2 = teamMapping[i['hTeam']['teamId']]
                        logo2 = teams[team2][0]
                        record2 = "(" + i['hTeam']['win'] + " - " + i['hTeam']['loss'] + ")"
                        score2 = i['hTeam']['score']
                        info.append([team1, logo1, record1, score1, team2, logo2, record2, score2, gameID])
    except:
        info = "NO GAMES"
    if len(info) == 0:
        info = "NO GAMES"
    return jsonify(info)

@app.route("/scores/")
def scores():
    return render_template("/scores.html")

@app.route("/results", methods = ["POST"])
def results():
    standings = getStandings()
    return jsonify(standings)

@app.route("/standings/")
def standings():
    return render_template("/standings.html")

@app.route("/updateNews", methods = ["POST"])
def updateNews():
    d2 = str(date.fromtimestamp(cTime))
    d1 = str(date.fromtimestamp(cTime - 604800))
    news = getNews(d1, d2)
    return jsonify(news)

@app.route("/news/")
def news():
    return render_template("/news.html")

@app.route("/playerInfo", methods = ["POST"])
def playerInfo():
    players, javascript = getPlayers()
    playerID = players[name][0]
    playerYear = players[name][1]
    stats = getStats(playerID, playerYear)
    if stats != "Error":
        stats.append(name)
    return jsonify(stats)

@app.route("/playerName", methods = ["POST"])
def playerName():
    global name
    global modified
    name = request.get_json()
    modified = name
    modified = modified.replace(" ", "-")
    return ''

@app.route("/players/<modified>/")
def players(modified):
    return render_template("players.html")

if __name__ == '__main__':
    app.run("0.0.0.0") 