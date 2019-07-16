from django.shortcuts import render

from ..models import Family


def families(request):
    fams = list(Family.objects.all().order_by("name"))

    for fam in list(fams):
        if fam.member_set.count() < 2:
            fams.remove(fam)

    return render(request, "teammanager/families.html", {
        "families": fams
    })
