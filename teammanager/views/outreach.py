import pytz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import timedelta, datetime

from teammanager import utils
from teammanager.models import Member, Meeting, Punch


@login_required
def add_event(request):
    if request.method == "POST":
        data = request.POST
        if 'name' in data and 'date' in data:
            m = Meeting(
                type='out',
                name=data['name'],
                date=data['date']
            )

            if 'desc' in data and data['desc']:
                m.description = data['desc']

            m.save()
            return redirect('man:meetings')
        else:
            return HttpResponse(status=403)

    else:
        return render(request, 'teammanager/outreach_event_add.html')


@login_required
def add_hours(request):
    members = Member.objects.all().order_by("first")
    if request.method == "POST":
        data = request.POST
        adding = []

        for element in data:
            if "mbr-" in element and data[element]:
                mid = int(element.split('-')[1])
                print(mid)
                q = Member.objects.filter(id=mid)
                if q.exists():
                    adding.append(q.first())

        print(adding)
        outreach = Meeting.objects.get(id=data["outreach-select"])

        for member in adding:
            start_time = timezone.datetime.combine(outreach.date, datetime.min.time())
            end_time = start_time + timedelta(hours=int(data['mbr-%s' % member.id]))
            print("start: {}, end: {}".format(start_time, end_time))

            try:
                punch = Punch.objects.get(member=member, meeting=outreach)
            except:
                punch = Punch(member=member, meeting=outreach)

            punch.start = start_time
            punch.end = end_time
            punch.fake = True

            if data["vol-%s" % member.id]:
                punch.volunteer_hrs = data["vol-%s" % member.id]

            punch.save()
            outreach.members.add(member)
        return redirect("man:outreach_hours_add")
    else:
        return render(request, 'teammanager/outreach_hours_add.html', {
            "members": members,
            "outreaches": Meeting.objects.filter(type="out").order_by("date").reverse()
        })

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
