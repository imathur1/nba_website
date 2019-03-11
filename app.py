import os
import json
import http.client
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    file = open("static/xml/upcoming/upcoming_" + str(year) + "_" + str(month) + "_" + str(day) + ".xml", "w")
    file.write(text)
    file.close()
    return str(year), str(month), str(day)

def deleteXML(year, month, day):
    value = 365 * year + 30 * month + day
    files = os.listdir("static/xml/upcoming/")
    for i in files:
        s = i.split("_")
        y = int(s[1])
        m = int(s[2])
        d = int(s[3][:-4])
        newValue = 365 * y + 30 * m + d
        if newValue < value:
            os.remove("static/xml/upcoming/" + i)

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
        deleteXML(int(a), int(b), int(c))
        tree = ET.parse("static/xml/upcoming/upcoming_" + a + "_" + b + "_" + c + ".xml")
        info = []
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
    return players, javascript

def getStats(playerID, year):
    stats = []
    with urllib.request.urlopen("http://data.nba.net/prod/v1/" + year + "/players/" + playerID + "_profile.json") as url:
        data = json.loads(url.read().decode())  
        for i in data['league']['standard']['stats']['regularSeason']['season']:
            for j in i['teams']:
                team = teamMapping[j['teamId']]
                logo = teams[team][1]
                points = float(j['ppg'])
                rebounds = float(j['rpg'])
                assists = float(j['apg'])
                minutes = float(j['mpg'])
                steals = float(j['spg'])
                turnovers = float(j['topg'])
                blocks = float(j['bpg'])
                totAssists = int(j['assists'])
                totBlocks = int(j['blocks'])
                totSteals = int(j['steals'])
                totTurnovers = int(j['turnovers'])
                totReb = int(j['totReb'])
                fieldGoalsMade = int(j['fgm'])
                fieldGoalsAttempted = int(j['fga'])
                fieldGoalPercent = float(j['fgp'])
                threePointsMade = int(j['tpm'])
                threePointsAttempted = int(j['tpa'])
                threePointPercent = float(j['tpp'])
                freeThrowsMade = int(j['ftm'])
                freeThrowsAttempted = int(j['fta'])
                freeThrowPercent = float(j['ftp'])
                personalFouls = int(j['pFouls'])
                totPoints = int(j['points'])
                gamesPlayed = int(j['gamesPlayed'])
                gamesStarted = int(j['gamesStarted'])
                totMinutes = int(j['min'])
                doubleDoubles = int(j['dd2'])
                tripleDoubles = int(j['td3'])
                stats.append([i['seasonYear'], logo, team, totMinutes, minutes, totPoints, points, 
                totAssists, assists, totReb, rebounds, totBlocks, blocks, totSteals, steals,
                totTurnovers, turnovers, threePointsMade, threePointsAttempted, threePointPercent,
                fieldGoalsMade, fieldGoalsAttempted, fieldGoalPercent, freeThrowsMade,
                freeThrowsAttempted, freeThrowPercent, personalFouls, gamesPlayed, gamesStarted,
                doubleDoubles, tripleDoubles])
                
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

    background = []
    n = name.split(" ")
    with urllib.request.urlopen("https://www.nba.com/players/" + n[0].lower() + "/" + n[1].lower() + "/" + playerID) as url:
        data = url.read().decode()
        parsed = BeautifulSoup(data, features='lxml')
        jersey = parsed.body.find('span', attrs={'class':'nba-player-header__jersey-number'}).text
        position = parsed.body.find('span', attrs={'class':'nba-player-header__position'}).text
        height = parsed.body.findAll('p', attrs={'class':'nba-player-vitals__top-info-imperial'})

        children1 = height[0].findChildren("span", recursive=False)
        height1 = children1[0].text + " " + children1[1].text
        children2 = height[1].findChildren("span", recursive=False)
        weight1 = children2[0].text
        
        info = parsed.body.findAll('span', attrs={'class':'nba-player-vitals__bottom-info'})
        born = info[0].text.strip()
        age = info[1].text.strip()
        from1 = info[2].text.strip()
        debut = info[3].text.strip()
        years = info[4].text.strip()
        image = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/" + playerID + ".png"
        background = [jersey, position, height1, weight1, born, age, from1, debut, years, image]

    stats.append(background)
    return stats

@app.route("/")
def output():
    return render_template("/index.html")

@app.route("/update", methods = ["POST"])
def update():
    info = request.get_json()
    offset = int(info[0])
    currentTime = getTime(info[1])
    upcoming = openStore(currentTime)
    a, b, c = openDate()
    upcoming = updateUpcoming(upcoming, currentTime, offset, a, b, c)
    return jsonify(upcoming)

@app.route("/updateAutocomplete", methods = ["POST"])
def updateAutocomplete():
    players, javascript = getPlayers()
    return jsonify(javascript)

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

@app.route("/playerInfo", methods = ["POST"])
def playerInfo():
    players, javascript = getPlayers()
    playerID = players[name][0]
    playerYear = players[name][1]
    stats = getStats(playerID, playerYear)
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
    app.run("0.0.0.0", "16")