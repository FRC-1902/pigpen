from datetime import timedelta

from django.shortcuts import render

from ..models import Member
from ..utils import time_to_string


def index(request):
    members = list(Member.objects.filter(active=True).order_by("-role", "first"))

    students = []

    hours_sum = timedelta()

    for member in members:
        hours = member.get_hours()
        hours_sum += hours.get("total")
        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                students.append({
                    "name": member.short_name(),
                    "hours": time_to_string(hours.get("total", "")),
                    "avatar": member.get_avatar(),
                    "raw_hours": hours.get("total"),
                    "id": member.id
                })

    students = sorted(students, key=lambda x: x['raw_hours'], reverse=True)

    return render(request, 'teammanager/index.html', {
                        "students": students[0:5],
                        "total_hours": time_to_string(hours_sum)
                   })
