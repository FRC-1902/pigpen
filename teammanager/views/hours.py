from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone

from pigpen import settings
from ..models import Member, Punch, Meeting
from ..utils import time_to_string

from pprint import pprint as print


def hours(request):
    return render(request, 'teammanager/hours.html')


def hours_table(request):
    members = list(Member.objects.filter(active=True).order_by("-role", "first"))

    head = ["Name", "Total", "Outreach", "Attendance"]
    students = []
    adults = []

    total_hours = Meeting.total_hours()

    for member in members:
        hours = member.get_hours()
        hours_delta = hours['build']

        attendance = int(hours_delta / total_hours * 100)
        # if attendance > 100:
        # attendance = 100

        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                students.append(tuple([
                    member,
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("out", 0)),
                    attendance,
                ]))
            elif member.role == 'mtr':
                adults.append(tuple([
                    member,
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("out", 0)),
                    attendance,
                ]))

    return render(request, 'teammanager/partial/hours_table.html', {
        "head": head,
        "students": students,
        "adults": adults,
    })


@login_required
def outreach_hours_add(request):
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


def getKey(item):
    return item[2]


def attendance_groups(request):
    members = list(Member.objects.exclude(role="asib").exclude(role="vip").order_by("-role", "first"))
    members_tuples = []
    students = []
    adults = []

    total_hours = Meeting.total_hours()

    zero_hours = []
    sub_30 = []
    sub_60 = []
    sub_90 = []
    wow = []

    for member in members:
        hours = member.get_hours()
        hours_delta = timedelta()

        attendance = int(hours['build'] / total_hours * 100)
        # if attendance > 100:
        # attendance = 100

        obj = (member, time_to_string(hours.get("total", "0")), attendance)
        members_tuples.append(obj)

    members_tuples = reversed(sorted(members_tuples, key=getKey))

    inactive = []
    for member in members_tuples:
        if member[0].active:
            attendance = member[2]
            if attendance == 0:
                zero_hours.append(member)
            elif attendance < 30:
                sub_30.append(member)
            elif attendance < 60:
                sub_60.append(member)
            elif attendance < 90:
                sub_90.append(member)
            else:
                wow.append(member)
        else:
            inactive.append(member)

    print(inactive)
    inactive = sorted(inactive, key=lambda x: x[0].first + x[0].last)

    return render(request, "teammanager/attendance_bands.html", {
        "groups": [("90%+", wow), ("(89% - 60%)", sub_90), ("(59% - 30%)", sub_60), ("(29% - 1%)", sub_30)],
        "zero": zero_hours,
        "inactive": inactive
    })
