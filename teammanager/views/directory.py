from django.shortcuts import render

from ..models import Family, Position


def directory(request):
    sections = []

    for pos in ["stoff", "tmldr", "stsub", "adsub", "stbus", "adbus", "adbod", "old"]:
        pos_list = Position.objects.filter(category=pos).order_by("sort")

        if pos_list.exists():
            sections.append({
                "title": pos_list.first().get_category_display(),
                "positions": list(pos_list)
            })

    return render(request, "teammanager/directory.html", {
        "sections": sections
    })


def families(request):
    fams = list(Family.objects.all().order_by("name"))
    singles = []

    for fam in list(fams):
        if fam.member_set.count() <= 1 and fam.member_set.all()[0].role != "old":
            singles = singles + list(fam.member_set.all())
            fams.remove(fam)

    return render(request, "teammanager/families.html", {
        "families": fams,
        "singles": singles,
    })
