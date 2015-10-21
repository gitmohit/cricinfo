import pynotify
from time import sleep
import requests
import optparse 
from bs4 import BeautifulSoup

def sendmessage(title, message):
    pynotify.init("Test")
    notice = pynotify.Notification(title, message)
    notice.show()
    return

def fetchscore(team1, team2, refreshTime):
    url = "http://static.cricinfo.com/rss/livescores.xml"
    while True:
        r = requests.get(url)
        while r.status_code is not 200:
            r = requests.get(url)
        soup = BeautifulSoup(r.text)
        data = soup.find_all("description")
        for d in data:
            stats = d.text.lower().strip(' ')
            if team1 in stats and team2 in stats:
                sendmessage("Score", d.text)
        sleep(refreshTime)

if __name__=='__main__':
    parser = optparse.OptionParser()
    parser.add_option('-a', '--teamA', type=str, action="store", dest="team1", default=None)
    parser.add_option('-b', '--teamB', type=str, action="store", dest="team2", default=None)
    parser.add_option('-t', '--refreshTime', type=int, action="store", dest="refresh_time", default=20)
    opts, args = parser.parse_args()
    teamA = opts.team1
    teamB = opts.team2
    refreshTime = opts.refresh_time
    if teamA and teamA:
        teamA = teamA.lower().strip(' ')
        teamB = teamB.lower().strip(' ')
        fetchscore(teamA,teamB,refreshTime)
    else:
        print 'Missing Arguments'
        exit(1)
