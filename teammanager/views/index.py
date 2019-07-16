from django.shortcuts import render

from ..models import Member, Punch


def index(request):

    members = list(Member.objects.order_by("-role", "first"))

    students = []

    for member in members:
        hours = member.get_hours()

        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                total = str(hours.get("total", "0")).split(":")
                total_string = "{}.{}".format(total[0], total[1])

                students.append(tuple([
                    member.short_name(),
                    total_string,
                    int(total[0]),
                    int(total[1]),
                    member.get_avatar()
                ]))


    students = sorted(students, key=lambda x: float(x[1]), reverse=True)

    return render(request, 'teammanager/index.html', {"students": students[0:5]})

def location(request):
    members = Member.objects.all().order_by("first")
    out = []
    members_in = [x.member for x in Punch.objects.filter(end__isnull=True)]

    for member in members:
        out.append({
            "id": member.id,
            "name": str(member),
            "position": member.role,
            "isIn": bool(member in members_in),
            "avatar": member.get_avatar()
        })
    return render(request, 'teammanager/location.html', {"members": out})