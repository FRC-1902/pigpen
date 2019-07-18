from django.contrib.auth.decorators import login_required
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
    total_meetings = len(Meeting.objects.filter(type="build"))

    for member in members:
        hours = member.get_hours()

        meetings = []

        punches = Punch.objects.filter(member=member)
        for punch in punches:
            if punch.meeting not in meetings:
                meetings.append(punch.meeting)
        attendance = int((len(meetings) / total_meetings) * 100)

        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                students.append(tuple([
                    member.short_name(),
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("out", 0)),
                    attendance,
                ]))
            else:
                adults.append(tuple([
                    member.short_name(),
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
