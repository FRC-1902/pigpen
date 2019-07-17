from django.shortcuts import render, redirect
from ..models import Member, Punch, Meeting


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


def meeting_breakdown(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except:
        return redirect("teammanager:meetings")
    punches = Punch.objects.filter(meeting=meeting)
    members = []
    punches_sorted = []
    for punch in punches:
        if punch.member not in members:
            members.append(punch.member)
        punches_sorted.append((punch.start, punch, "in"))
        punches_sorted.append((punch.end, punch, "out"))
    punches_sorted = sorted(punches_sorted)

    return render(request, "teammanager/meeting.html", {
        "members": members,
        "meeting": meeting,
        "punches": punches_sorted
    })


def meetings(request):
    meetings = Meeting.objects.all().order_by("date")
    return render(request, "teammanager/meetings.html", {"meetings": meetings})