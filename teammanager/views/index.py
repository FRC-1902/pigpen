from django.shortcuts import render

from ..models import Member
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
