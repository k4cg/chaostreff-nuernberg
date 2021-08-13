#!/usr/bin/env python3

from dateutil.rrule import rrule, WEEKLY, MONTHLY, TH, TU, MO, WE
from datetime import datetime, date, timedelta

import urllib.request
import icalendar
import recurring_ical_events


FABLAB_ACTIVE=True
K4CG_ACTIVE=True
NERDBERG_ACTIVE=True



class Entry:
    def __init__(self, date: datetime, location: str, time: str):
        self.date = date
        self.location = location
        self.time = time

    def __repr__(self):
        return str(self.date) + ' ' + self.location + ' ' + self.time

    def asHTML(self):
        template = '<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
        dateString = self.date.strftime('%d.%m.%Y')
        return template % (dateString, self.location, self.time)


def k4cgEntry(date: datetime):
    return Entry(date, 'K4CG', '19:30 - 22:00')


def fablabEntry(date: datetime):
    return Entry(date, 'Fablab Region Nürnberg', '19:30 - 22:00')

def nerdbergEntry(date: datetime):
    return Entry(date, 'Nerdberg', '19:00 - 22:00')

def calcEntries():
    today = datetime.today()
    
    count = 5
    dates = []
    maxDate = []
    
    if K4CG_ACTIVE:
        k4cg = list(rrule(MONTHLY, count=count, byweekday=TH(1), dtstart=today, wkst=MO))
        for dateEntry in k4cg:
            dates.append(k4cgEntry(dateEntry))
            maxDate.append(dateEntry)

    if FABLAB_ACTIVE:
        fablab = list(rrule(MONTHLY, count=count, byweekday=TU(3), dtstart=today, wkst=MO))
        for dateEntry in fablab:
            dates.append(fablabEntry(dateEntry))
            maxDate.append(dateEntry)

    if NERDBERG_ACTIVE:
        if len(maxDate) == 0:
            maxDate.append(today + timedelta(weeks=12))
        ical_string = urllib.request.urlopen("https://kalender.nerdberg.de/events.ics").read()
        calendar = icalendar.Calendar.from_ical(ical_string)
        events = recurring_ical_events.of(calendar).between(today, max(maxDate))
        for event in events:
            if event['Summary'] == "Chaostreff":
                dates.append(nerdbergEntry(event['dtstart'].dt.replace(tzinfo=None)))

    dates.sort(key=lambda entry: entry.date)

    for dateEntry in dates:
        yield dateEntry.asHTML()


if __name__ == "__main__":
    fin = open("template.html", "r")
    data = fin.read()
    data = data.replace('{{data}}', "".join(calcEntries()))
    fin.close()
    fin = open("index.html", "w")
    fin.write(data)
    fin.close()
