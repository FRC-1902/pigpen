from django.shortcuts import render

from ..models import Family


def families(request):
    fams = list(Family.objects.all().order_by("name"))
    singles = []

    for fam in list(fams):
        if fam.member_set.count() <= 1:
            singles = singles + list(fam.member_set.all())
            fams.remove(fam)

    fams = sorted(fams, key=lambda x: x.member_set.count(), reverse=True)

    return render(request, "teammanager/families.html", {
        "families": fams,
        "singles": singles,
    })
