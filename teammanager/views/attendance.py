from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from pigpen import settings
from teammanager import utils
from ..models import Member, Punch, Meeting
from ..utils import time_to_string


def whos_in(request):
    members = list(Member.objects.filter(active=True).order_by("first", "last"))
    out = []
    members_in = [x.member for x in Punch.objects.filter(end__isnull=True, meeting__type="build")]

    for m in members_in:
        if m not in members:
            members.append(m)

    members = sorted(members, key=lambda x: x.first + x.last)

    for member in members:
        out.append({
            "id": member.id,
            "name": member.short_name(),
            "position": member.role,
            "isIn": bool(member in members_in),
            "avatar": member.get_avatar()
        })
    return render(request, 'teammanager/attendance_whos_in.html', {
        "members": out,
        "any_checkins": len(members_in) > 0
    })


def meeting_breakdown(request, id):
    try:
        meeting = Meeting.objects.get(id=id)
    except:
        return redirect("teammanager:meetings")

    punches = Punch.objects.filter(meeting=meeting)

    punches_sorted = []
    fakes = False
    for punch in punches:
        if punch.fake:
            if punch.is_complete():
                fakes = True
                punches_sorted.append((time_to_string(punch.duration()), punch))
        else:
            if punch.start:
                punches_sorted.append((punch.start, punch, "in"))
            if punch.end:
                punches_sorted.append((punch.end, punch, "out"))

    if not fakes:
        punches_sorted = sorted(punches_sorted, key=lambda x: x[0])

    return render(request, "teammanager/meeting.html", {
        "members": meeting.members.order_by("first", "last"),
        "meeting": meeting,
        "punches": punches_sorted
    })


@csrf_exempt
def meetings(request):
    if request.method == "POST":
        try:
            member = Member.objects.get(id=request.session["member"])
        except:
            return JsonResponse({
                "success": False,
                "error": "Invalid member session."
            })
        data = request.POST
        if "signup" in data:
            id = data["signup"]
            try:
                meeting = Meeting.objects.get(id=id, type="out")
            except:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid meeting id or wrong meeting type."
                })
            meeting.members.add(member)
            return JsonResponse({
                "success": True
            })
    else:
        member = None
        if "member" in request.session:
            try:
                member = Member.objects.get(id=request.session["member"])
            except:
                print("Failed to get member")
        now = timezone.now()
        #meetings = Meeting.objects.filter(date__lte=now).order_by("date").reverse()
        meetings = Meeting.objects.all().order_by("date").reverse()
        outreaches_upcoming = Meeting.objects.filter(type="out", date__gte=now).order_by("date")
        outreaches_old = Meeting.objects.filter(type="out", date__lt=now).order_by("date").reverse()
        return render(request, "teammanager/meeting_list.html", {
            "meetings": meetings,
            "outreaches_upcoming": outreaches_upcoming,
            "outreaches_old": outreaches_old,
            "member": member
        })


def member(request, id):
    try:
        member = Member.objects.get(id=id)
    except Exception as e:
        print(e)
        return redirect("teammanager:index")

    build_meetings = []
    meetings = []
    outreaches_processed = []
    outreaches = []

    total_hours = Meeting.total_hours()
    total_meetings = list(Meeting.meetings_since_cutoff())

    hours = timedelta()
    punches = Punch.objects.filter(member=member, start__gt=settings.attendance_start_date).order_by("start").reverse()
    for punch in punches:
        if punch.is_complete() and (punch.meeting.type == "build" or punch.meeting.type == "othr"):
            hours += punch.duration()
        if punch.meeting not in meetings and (punch.meeting.type == "build" or punch.meeting.type == "othr"):
            meetings.append(punch.meeting)
            if punch.meeting.type == "build":
                build_meetings.append(punch.meeting)
        if punch.meeting.type == "out" and punch.meeting not in outreaches_processed:
            outreaches_processed.append(punch.meeting)
            sum = punch.meeting.hours_sum(member)
            if sum:
                outreaches.append((punch.meeting, time_to_string(sum)))
            else:
                outreaches.append((punch.meeting, None))

    #meetings.reverse()
    attend = int(hours / total_hours * 100)
    # if attend > 100:
    # attend = 100
    family = Member.objects.filter(family=member.family)

    hours = member.get_hours()
    return render(request, "teammanager/member_attendance.html", {
        "member": member,
        "meetings": meetings,
        "build_meetings": build_meetings,
        "outreaches": outreaches,
        "total_meetings": len(total_meetings),
        "attendance_percent": attend,
        "hr_total": time_to_string(hours.get("total", "0")),
        "hr_build": time_to_string(hours.get("build", "0")),
        "hr_out": time_to_string(hours.get("out", "0")),
        "family": family
    })


@staff_member_required
def meetings_verify(request):
    if 'id' in request.GET:
        try:
            m = Meeting.objects.get(id=request.GET['id'])
            m.verified = True
            m.save()
        except:
            pass
        return redirect("man:meetings_verify")
    else:
        meetings = []
        now = timezone.now()
        for meeting in Meeting.objects.filter(verified=False).filter(date__lt=now).order_by("date"):
            if not meeting.name:
                meeting.name = ""
            meeting.date_str = meeting.date.strftime(utils.date_fmt)
            meetings.append(meeting)

        return render(request, "teammanager/meeting_verification.html", {
            "meetings": meetings
        })


def no_slack_list(request):
    members = Member.objects.filter(slack__isnull=True)
    return render(request, "teammanager/no_slack_list.html", {
        "members": members
    })
