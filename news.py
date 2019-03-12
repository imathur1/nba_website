from newsapi import NewsApiClient

teams = {
    "Cleveland Cavaliers": "CLE",
    "Detroit Pistons": "DET",
    "Indiana Pacers": "IND",
    "Orlando Magic": "ORL",
    "Miami Heat": "MIA",
    "Brooklyn Nets": "BKN",
    "Philadelphia 76ers": "PHI",
    "Golden State Warriors": "GSW",
    "Dallas Mavericks": "DAL",
    "Memphis Grizzlies": "MEM",
    "San Antonio Spurs": "SAS",
    "Oklahoma City Thunder": "OKC", 
    "Utah Jazz": "UTA",
    "Milwaukee Bucks": "MIL",
    "Phoenix Suns": "PHX",
    "Los Angeles Lakers": "LAL",
    "Denver Nuggets": "DEN",
    "New Orleans Pelicans": "NOP",
    "Sacramento Kings": "SAC",
    "Los Angeles Clippers": "LAC",
    "Chicago Bulls": "CHI",
    "Portland Trail Blazers": "POR",
    "Boston Celtics": "BOS",
    "Minnesota Timberwolves": "MIN",
    "Atlanta Hawks": "ATL",
    "Washington Wizards": "WAS",
    "Houston Rockets": "HOU",
    "Charlotte Hornets": "CHA",
    "Toronto Raptors": "TOR",
    "New York Knicks": "NYK"
}

newsapi = NewsApiClient(api_key='7477d1d0e72844348ebc6472a323c125')

top_headlines = newsapi.get_top_headlines(q='nba',
                                          category='sports',
                                          language='en',
                                          country='us')

all_articles = newsapi.get_everything(q='nba',
                                      sources='espn,bleacher-report',
                                      domains='espn.com,bleacherreport.com,nba.com',
                                      from_param='2019-03-04',
                                      to='2019-03-11',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

seen = []
data = []
articles1 = top_headlines['articles']
articles2 = all_articles['articles']
for i in articles1:
    source = i['source']['name']
    author = i['author']
    title = i['title']
    description = i['description']
    url = i['url']
    image = i['urlToImage']
    time = i['publishedAt']
    content = i['content']
    if source == 'Espn.com' or source == 'Nba.com' or source == 'Bleacher Report':
        if url not in seen:
            seen.append(url)
            data.append([source, author, title, description, url, image, time, content])

for i in articles2:
    source = i['source']['name']
    author = i['author']
    title = i['title']
    description = i['description']
    url = i['url']
    image = i['urlToImage']
    time = i['publishedAt']
    content = i['content']
    if url not in seen:
        seen.append(url)
        data.append([source, author, title, description, url, image, time, content])