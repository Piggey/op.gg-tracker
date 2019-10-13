from time import sleep
from requests import get
from bs4 import BeautifulSoup

test_url = 'https://eune.op.gg/summoner/userName=gigakoksjungler'
matchList = []
url = input('op.gg link: ')
if(url == 'test'):
    url = test_url
Won = int(input("Matches already won: "))
Lost = int(input("Matches already lost: "))
Interval = int(input("Minutes of interval inbetween checking: "))

def CheckMatches():
    #### Disa powinno sie jebac ####
    V, D = 0, 0
    old_matchList = matchList.copy()
    matchList.clear()
    comparsion = []
    page = get(url)
    matches = BeautifulSoup(page.content, 'html.parser').find_all('div', {'class': 'GameResult'})

    for match in matches:
        outcome = match.get_text().strip('\n																				 ')
        matchList.append(outcome)
    
    for match in matchList:
        if(match not in old_matchList):
            comparsion.append(match)

    #print(comparsion)
    for match in comparsion:
        if(match == 'Victory'):
            V += 1
        elif(match == 'Defeat'):
            D += 1

    return V, D

def CheckLeague():
    page = get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tier = soup.find('div', {'class': 'TierRank'}).get_text()
    LP = soup.find('span', {'class': 'LeaguePoints'}).get_text().strip('\n				 LP\n			')

    return f'{tier[0]} {LP}LP'

#setup the matchlist:
print("Tracking started!")
CheckMatches()

#proper checking:
while(True):
    stats = open("stats.txt", 'w')
    league = open("league.txt", 'w')

    res = CheckMatches()
    Won += res[0]
    Lost += res[1]

    stats.write(f'{Won}/{Lost}')
    league.write(CheckLeague())
    stats.close()
    league.close()

    sleep(Interval * 60)