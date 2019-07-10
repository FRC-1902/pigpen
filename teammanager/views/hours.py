from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Member


def hours(request):
    return render(request, 'teammanager/hours.html')


def hours_table(request):
    sort_leader = bool(request.GET.get('sort', 'default') == "leader")
    members = list(Member.objects.order_by("-role", "first"))

    head = ["Name", "Total", "Build", "Outreach"]
    students = []
    adults = []

    for member in members:
        hours = member.get_hours()
        if member.role == 'stu':
            students.append(tuple([
                member.short_name(),
                str(hours.get("total", "0")).split(':')[0],
                str(hours.get("build", "0")).split(':')[0],
                str(hours.get("out", 0)).split(':')[0]
            ]))
        else:
            adults.append(tuple([
                member.short_name(),
                str(hours.get("total", "0")).split(':')[0],
                str(hours.get("build", "0")).split(':')[0],
                str(hours.get("out", 0)).split(':')[0]
            ]))

    if sort_leader:
        students = sorted(students, key=lambda x: int(x[1]))
        adults = sorted(students, key=lambda x: int(x[1]))

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
