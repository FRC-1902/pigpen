import pytz
from django.shortcuts import render
from django.utils import timezone

from teammanager import utils


def create_outreach_from_calendar(request):
    if request.method == "GET":
        tz = pytz.timezone("America/New_York")

        c = utils.get_calendar()

        events = []
        for event in c.events:
            if event.begin > timezone.now() and "OPEN" not in event.name and not event.all_day:
                event.date_str = event.begin.astimezone(tz).strftime(utils.date_fmt)
                event.time_start_str = event.begin.astimezone(tz).strftime(utils.time_fmt)
                event.time_end_str = event.end.astimezone(tz).strftime(utils.time_fmt)
                events.append(event)

        return render(request, "teammanager/outreach_from_calendar.html", {
            "events": events,
        })
    else:
        pass
