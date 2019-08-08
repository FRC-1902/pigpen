from django.shortcuts import render

from ..models import Member, Family, Position


def directory(request):
    students = list(Member.objects.filter(role="stu").order_by("first"))
    mentors = list(Member.objects.filter(role="mtr").order_by("first"))

    return render(request, "teammanager/directory_all.html", {
        "students": students,
        "adults": mentors
    })


def leaders(request):
    sections = []

    for pos in ["stoff", "tmldr", "stsub", "adsub", "stbus", "adbus", "adbod", "old"]:
        pos_list = Position.objects.filter(category=pos).order_by("sort")

        if pos_list.exists():
            sections.append({
                "title": pos_list.first().get_category_display(),
                "positions": list(pos_list)
            })

    return render(request, "teammanager/directory_leaders.html", {
        "sections": sections
    })


def families(request):
    fams = list(Family.objects.all().order_by("name"))
    singles = []

    for fam in list(fams):
        if fam.member_set.count() <= 1:
            if fam.member_set.exists() and fam.member_set.all()[0].role != "ext":
                singles = singles + list(fam.member_set.all())
            fams.remove(fam)

    return render(request, "teammanager/directory_families.html", {
        "families": fams,
        "singles": singles,
    })


def staff_list(request):
    members = Member.objects.all().order_by("first")

    head = ["Name", "Role", "Avatar", "Slack"]
    out = []
    for member in members:
        out.append((
            member,
            member.get_role_display(),
            bool(member.avatar),
            member.slack_username if bool(member.slack_username) else "",
        ))

    return render(request, "teammanager/directory_staff.html", {
        "head": head,
        "members": out
    })
