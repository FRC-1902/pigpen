from django.shortcuts import render

from ..models import Member, Punch
from ..utils import time_to_string


def index(request):
    members = list(Member.objects.order_by("-role", "first"))

    students = []

    for member in members:
        hours = member.get_hours()

        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                students.append({
                    "name": member.short_name(),
                    "hours": time_to_string(hours.get("total", "")),
                    "avatar": member.get_avatar(),
                    "raw_hours": hours.get("total")
                })

    students = sorted(students, key=lambda x: x['raw_hours'], reverse=True)

    return render(request, 'teammanager/index.html', {"students": students[0:5]})


def location(request):
    members = Member.objects.all().order_by("first", "last")
    out = []
    members_in = [x.member for x in Punch.objects.filter(end__isnull=True)]

    for member in members:
        out.append({
            "id": member.id,
            "name": member.short_name(),
            "position": member.role,
            "isIn": bool(member in members_in),
            "avatar": member.get_avatar()
        })
    return render(request, 'teammanager/location.html', {
        "members": out,
        "any_checkins": len(members_in) > 0
    })
