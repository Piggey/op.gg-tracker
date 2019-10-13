from time import sleep
from requests import get
from bs4 import BeautifulSoup

match = KDA = ''
test_url = 'https://euw.op.gg/summoner/userName=GIGAKLOCJUNGLER'
url = input('op.gg link: ')
if(url == 'test'):
    url = test_url

Won = input("Matches already won (type 'l' to load previous Win/Loss stats from stats.txt file): ")
if(Won == 'l'):
    stat = open("stats.txt").read().split("/")
    Won = int(stat[0])
    Lost = int(stat[1])
    print(Won, Lost)
else:
    Won = int(Won)
    Lost = int(input("Matches already lost: "))

Interval = int(input("Minutes of interval inbetween checking: "))

def CheckMatches():
    #### Disa powinno sie jebac ####
    global match
    global KDA
    prev_match = match
    prev_KDA = KDA
    page = get(url)
    sup = BeautifulSoup(page.content, 'html.parser')
    match = sup.find('div', {'class': 'GameResult'}).get_text().strip('\n																				 ')
    KDA = sup.find('span', {'class': 'KDARatio'}).get_text()

    if(prev_KDA != KDA and prev_match != match):
        print("New activity has been tracked.")
        if(match == "Victory"):
            return (1,0)
        elif(match == "Defeat"):
            return (0,1)
    else:
        return (0,0)



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