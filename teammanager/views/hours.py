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


def getKey(item):
    return item[2]

def attendance_groups(request):
    members = list(Member.objects.order_by("-role", "first"))
    members_tuples = []
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
        if not member.role == "asib" and not member.role == "ext":
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
            members_tuples.append(obj)

    members_tuples = reversed(sorted(members_tuples, key=getKey))

    for member in members_tuples:
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


    return render(request, "teammanager/clusters.html", {
        "groups": [("90%+", wow), ("(60% - 89%)", sub_90), ("(30% - 59%)", sub_60), ("(1% - 29%)", sub_30)],
        "zero": zero_hours
    })