from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from ..models import Member, Punch, Meeting
from ..utils import time_to_string


def hours(request):
    return render(request, 'teammanager/hours.html')


def hours_table(request):
    members = list(Member.objects.order_by("-role", "first"))

    head = ["Name", "Total", "Outreach", "Attendance"]
    students = []
    adults = []
    total_meetings = Meeting.objects.filter(type="build")
    total_hours = total_meetings.aggregate(Sum('length'))['length__sum']
    total_hours = timedelta(hours=total_hours)

    for member in members:
        hours = member.get_hours()
        hours_delta = timedelta()

        meetings = []

        punches = Punch.objects.filter(member=member)
        for punch in punches:
            if punch.is_complete():
                hours_delta += punch.duration()
            if punch.meeting not in meetings:
                meetings.append(punch.meeting)
        attendance = int(hours_delta/total_hours * 100)
        #if attendance > 100:
            #attendance = 100

        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                students.append(tuple([
                    member,
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("out", 0)),
                    attendance,
                ]))
            else:
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
    return render(request, 'teammanager/outreach_hours_add.html', {
        "members": members
    })


def attendance_groups(request):
    members = list(Member.objects.order_by("-role", "first"))

    students = []
    adults = []
    total_meetings = Meeting.objects.filter(type="build")
    total_hours = total_meetings.aggregate(Sum('length'))['length__sum']
    total_hours = timedelta(hours=total_hours)

    zero_hours = []
    sub_30 = []
    sub_60 = []
    sub_90 = []
    wow = []

    for member in members:
        if not member.role == "asib":
            hours = member.get_hours()
            hours_delta = timedelta()

            meetings = []

            punches = Punch.objects.filter(member=member)
            for punch in punches:
                if punch.is_complete():
                    hours_delta += punch.duration()
                if punch.meeting not in meetings:
                    meetings.append(punch.meeting)
            attendance = int(hours_delta / total_hours * 100)
            # if attendance > 100:
            # attendance = 100

            obj = (member, time_to_string(hours.get("total", "0")), attendance)
            if attendance == 0:
                zero_hours.append(obj)
            elif attendance < 30:
                sub_30.append(obj)
            elif attendance < 60:
                sub_60.append(obj)
            elif attendance < 90:
                sub_90.append(obj)
            else:
                wow.append(obj)


    return render(request, "teammanager/clusters.html", {
        "groups": [("90%+", wow), ("60%+", sub_90), ("30%+", sub_60), ("1%+", sub_30)],
        "zero": zero_hours
    })