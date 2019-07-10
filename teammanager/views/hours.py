from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from ..models import Member


@login_required
def hours(request):
    return render(request, 'teammanager/hours.html')


@login_required
def hours_table(request):
    members = list(Member.objects.order_by("-role", "first"))

    head = ["Name", "Build", "Outreach"]
    students = []
    adults = []

    for member in members:
        hours = member.get_hours()
        if member.role == 'stu':
            students.append(tuple([
                member.short_name(),
                str(hours.get("build", "0")).split(':')[0],
                str(hours.get("out", 0)).split(':')[0]
            ]))
        else:
            adults.append(tuple([
                member.short_name(),
                str(hours.get("build", "0")).split(':')[0],
                str(hours.get("out", 0)).split(':')[0]
            ]))

    return render(request, 'teammanager/partial/hours_table.html', {
        "head": head,
        "students": students,
        "adults": adults,
    })


def outreach_hours_add(request):
    members = Member.objects.all().order_by("first")
    return render(request, 'teammanager/outreach_hours_add.html', {
        "members": members
    })
