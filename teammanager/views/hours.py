from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from ..models import Member, Punch, Meeting
from ..utils import time_to_string


def hours(request):
    return render(request, 'teammanager/hours.html')


def hours_table(request):
    members = list(Member.objects.filter(active=True).order_by("-role", "first"))

    head = ["Name", "Total", "Outreach", "Attendance"]
    students = []
    adults = []
    total_meetings = Meeting.objects.filter(type="build")
    total_hours = total_meetings.aggregate(Sum('length'))['length__sum']
    total_hours = timedelta(hours=total_hours)

    for member in members:
        hours = member.get_hours()
        hours_delta = timedelta()

        punches = Punch.objects.filter(member=member)
        for punch in punches:
            if punch.is_complete() and (punch.meeting.type == "build" or punch.meeting.type == "othr"):
                hours_delta += punch.duration()

        attendance = int(hours_delta/total_hours * 100)
        #if attendance > 100:
            #attendance = 100

        if int(hours.get("total", "0").seconds) > 0:
            if member.role == 'stu':
                students.append(tuple([
                    member,
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("out", 0)),
                    attendance,
                ]))
            elif member.role == 'mtr':
                adults.append(tuple([
                    member,
                    time_to_string(hours.get("total", "0")),
                    time_to_string(hours.get("out", 0)),
                    attendance,
                ]))

    return render(request, 'teammanager/partial/hours_table.html', {
        "head": head,
        "students": students,
        "adults": adults,
    })


@login_required
def outreach_hours_add(request):
    members = Member.objects.all().order_by("first")
    if request.method == "POST":
        data = request.POST
        print(data)
        adding = []
        for member in members:
            if "mbr-{}".format(member.id) in data and member not in adding:
                adding.append(member)
        hours = float(data["num_hrs"])
        print("Hours: " + str(hours))
        outreach = Meeting.objects.get(id=data["outreach-select"])

        for member in adding:
            start_time = datetime.combine(outreach.date, datetime.min.time())
            end_time = start_time + timedelta(hours=hours)
            print("start: {}, end: {}".format(start_time, end_time))

            try:
                punch = Punch.objects.get(member=member, meeting=outreach)
            except:
                punch = Punch(member=member, meeting=outreach)

            punch.start = start_time
            punch.end = end_time
            punch.fake = True
            punch.save()
            outreach.members.add(member)
        return redirect("man:outreach_hours_add")
    else:
        return render(request, 'teammanager/outreach_hours_add.html', {
            "members": members,
            "outreaches": Meeting.objects.filter(type="out").order_by("date").reverse()
        })


def getKey(item):
    return item[2]


def attendance_groups(request):
    members = list(Member.objects.filter(active=True).order_by("-role", "first"))
    members_tuples = []
    students = []
    adults = []
    total_meetings = Meeting.objects.filter(type="build")
    total_hours = total_meetings.aggregate(Sum('length'))['length__sum']
    total_hours = timedelta(hours=total_hours)

    zero_hours = []
    sub_30 = []
    sub_60 = []
    sub_90 = []
    wow = []

    for member in members:
        if not member.role == "asib" and not member.role == "vip":
            hours = member.get_hours()
            hours_delta = timedelta()

            meetings = []

            punches = Punch.objects.filter(member=member)
            for punch in punches:
                if punch.is_complete() and (punch.meeting.type == "build" or punch.meeting.type == "othr"):
                    hours_delta += punch.duration()
                if punch.meeting not in meetings and punch.meeting.type == "build":
                    meetings.append(punch.meeting)
            attendance = int(hours_delta / total_hours * 100)
            # if attendance > 100:
            # attendance = 100

            obj = (member, time_to_string(hours.get("total", "0")), attendance)
            members_tuples.append(obj)

    members_tuples = reversed(sorted(members_tuples, key=getKey))

    for member in members_tuples:
        attendance = member[2]
        if attendance == 0:
            zero_hours.append(member)
        elif attendance < 30:
            sub_30.append(member)
        elif attendance < 60:
            sub_60.append(member)
        elif attendance < 90:
            sub_90.append(member)
        else:
            wow.append(member)

    return render(request, "teammanager/attendance_bands.html", {
        "groups": [("90%+", wow), ("(60% - 89%)", sub_90), ("(30% - 59%)", sub_60), ("(1% - 29%)", sub_30)],
        "zero": zero_hours
    })