from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Member


@login_required
def hours(request):
    return render(request, 'teammanager/hours.html')


@login_required
def hours_table(request):
    members = list(Member.objects.all())

    head = ["Name", "Build", "Outreach"]
    out = []

    for member in members:
        hours = member.get_hours()
        out.append(tuple([str(member), hours.get("build", 0), hours.get("out", 0)]))

    return render(request, "teammanager/partial/hours_table.html", {
        "head": head,
        "rows": out
    })
