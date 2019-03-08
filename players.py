# Run this every season to update the teams database
"""
import time
import http.client
import xml.etree.ElementTree as ET

conn = http.client.HTTPSConnection("api.sportradar.us")
conn.request("GET", "/nba/trial/v5/en/league/hierarchy.xml?api_key=rafgw5sffp5tj5g437uhc7we")
res = conn.getresponse()
data = res.read()
text = data.decode("utf-8")
file = open("static/xml/players/league.xml", "w")
file.write(text)
file.close()

players = dict()
file = open("static/database/players.txt", "r")
num = int(file.readline().strip("\n"))
for i in range(num):
    key = file.readline().strip("\n")
    value = file.readline().strip("\n")
    players[key] = value
file.close()

teams = []
tree = ET.parse("static/xml/players/league.xml")
for elem in tree.iter():
    if elem.tag == "{http://feed.elasticstats.com/schema/basketball/nba/hierarchy-v5.0.xsd}team":
        teams.append(elem.attrib['id'])

conn = http.client.HTTPSConnection("api.sportradar.us")
count = 0
for i in teams:
    conn.request("GET", "/nba/trial/v5/en/teams/" + i + "/profile.xml?api_key=rafgw5sffp5tj5g437uhc7we")
    res = conn.getresponse()
    data = res.read()
    text = data.decode("utf-8")
    file = open("static/xml/players/players.xml", "w")
    file.write(text)
    file.close()

    tree = ET.parse("static/xml/players/players.xml")
    for elem in tree.iter():
        if elem.tag == "{http://feed.elasticstats.com/schema/basketball/team-v2.0.xsd}player":
            key = elem.attrib['full_name']
            value = elem.attrib['id']
            if not value in players.values():
                players[key] = value
    count += 1
    time.sleep(2)

file = open("static/database/players.txt", "w")
file.write(str(len(players)) + "\n")
for i in players:
    file.write(i + "\n")
    file.write(players[i] + "\n")
file.close()
"""