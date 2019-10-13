#!/usr/bin/env python3

from dateutil.rrule import rrule, MONTHLY, TH, TU
from datetime import datetime, date


class Entry:
    def __init__(self, date: datetime, location: str, time: str):
        self.date = date
        self.location = location
        self.time = time

    def __repr__(self):
        return str(self.date) + ' ' + self.location + ' ' + self.time

    def asHTML(self):
        template = '<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
        dateString = self.date.strftime('%Y-%m-%d')
        return template % (dateString, self.location, self.time)


def k4cgEntry(date: datetime):
    return Entry(date, 'K4CG', '19:30 - 22:00')


def fablabEntry(date: datetime):
    return Entry(date, 'Fablab Region Nürnberg', '19:30 - 22:00')


today = date.today()

count = 5
dates = []

k4cg = list(rrule(MONTHLY, count=count, byweekday=TH(1), dtstart=today))
for dateEntry in k4cg:
    dates.append(k4cgEntry(dateEntry))

fablab = list(rrule(MONTHLY, count=count, byweekday=TU(3), dtstart=today))
for dateEntry in fablab:
    dates.append(fablabEntry(dateEntry))

dates.sort(key=lambda entry: entry.date)

for dateEntry in dates:
    print(dateEntry.asHTML())
