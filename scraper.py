import urllib.request
import re
from bs4 import BeautifulSoup
from datetime import datetime


class Events:
    def __init__(self):
        self.soup = self.getSoup()
        self.events = self.getEvents(self.soup)

    def getSoup(self):
        url = 'http://www.americanairlinescenter.com/events'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        req = urllib.request.Request(url, None, headers)

        with urllib.request.urlopen(req) as response:
            return BeautifulSoup(response.read(), "html.parser")

    def getEvents(self, soup):
        divs = soup.find_all('div', 'info clearfix')
        events = []
        for i in range(len(divs)):
            dateRegex = '<div class="date">\s+(.+)\s+-\s(.+)\s+</div>'
            div = str(divs[i])
            date, time = re.findall(dateRegex, div)[0]
            date = date.strip()
            time = time.strip()
            if len(time) <= 3:
                time = f'{time[:1]}:00{time[1:]}'
            eventRegex = 'title="More Info">(.*)</a>'
            event = re.findall(eventRegex, div)[0]

            dt = datetime.strptime(' '.join([date, time]), '%b %d, %Y %I:%M%p')
            events.append((event, dt))
        return events
