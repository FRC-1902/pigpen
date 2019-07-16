from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Member
from ..utils import time_to_string


def hours(request):
    return render(request, 'teammanager/hours.html')


def hours_table(request):
    members = list(Member.objects.order_by("-role", "first"))

    head = ["Name", "Total", "Build", "Outreach"]
    students = []
    adults = []

    for member in members:
        hours = member.get_hours()

        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                students.append(tuple([
                    member.short_name(),
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("build", "0")),
                    time_to_string(hours.get("out", 0)),
                ]))
            else:
                adults.append(tuple([
                    member.short_name(),
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("build", "0")),
                    time_to_string(hours.get("out", 0)),
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
