import pytz
import requests

from django.shortcuts import render
from django.utils import timezone

from ics import Calendar


def create_outreach_from_calendar(request):
    if request.method == "GET":
        url = "https://calendar.google.com/calendar/ical/explodingbacon.team1902%40gmail.com/public/basic.ics"
        date_fmt = "%a %b %-d, %Y"
        time_fmt = "%-I:%M %p"
        c = Calendar(requests.get(url).text)
        tz = pytz.timezone("America/New_York")

        events = []
        for event in c.events:
            if event.begin > timezone.now() and "OPEN" not in event.name and not event.all_day:
                event.date_str = event.begin.astimezone(tz).strftime(date_fmt)
                event.time_start_str = event.begin.astimezone(tz).strftime(time_fmt)
                event.time_end_str = event.end.astimezone(tz).strftime(time_fmt)
                events.append(event)

        return render(request, "teammanager/outreach_from_calendar.html", {
            "events": events,
        })
    else:
        pass
