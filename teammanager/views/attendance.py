from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import render, redirect

from ..models import Member, Punch, Meeting
from ..utils import time_to_string


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
        if punch.end:
            punches_sorted.append((punch.end, punch, "out"))
    punches_sorted = sorted(punches_sorted)

    return render(request, "teammanager/meeting.html", {
        "members": members,
        "meeting": meeting,
        "punches": punches_sorted
    })


def meetings(request):
    meetings = Meeting.objects.all().order_by("date").reverse()
    return render(request, "teammanager/meetings.html", {"meetings": meetings})


def member(request, id):
    try:
        member = Member.objects.get(id=id)
    except Exception as e:
        print(e)
        return redirect("teammanager:index")
    meetings = []
    total_meetings = Meeting.objects.filter(type="build")
    total_hours = total_meetings.aggregate(Sum('length'))['length__sum']
    total_hours = timedelta(hours=total_hours)
    hours = timedelta()
    punches = Punch.objects.filter(member=member)
    for punch in punches:
        if punch.is_complete():
            hours += punch.duration()
        if punch.meeting not in meetings:
            meetings.append(punch.meeting)

    meetings.reverse()
    attend = int(hours / total_hours * 100)
    # if attend > 100:
    # attend = 100

    hours = member.get_hours()
    return render(request, "teammanager/member_attendance.html", {
        "member": member,
        "meetings": meetings,
        "total_meetings": len(total_meetings),
        "attendance_percent": attend,
        "hr_total": time_to_string(hours.get("total", "0")),
        "hr_build": time_to_string(hours.get("build", "0")),
        "hr_out": time_to_string(hours.get("out", "0"))
    })
