import os

from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..models import Family, Position


@csrf_exempt
def directory(request):
    if request.method == 'GET' and not request.user.is_authenticated:
        return render(request, 'teammanager/directory_login.html')
    else:
        if request.user.is_authenticated or request.POST.get("passcode", "none") == os.getenv("DIRECTORY_PASSCODE",
                                                                                              "\n"):
            sections = []

            for pos in ["stoff", "tmldr", "stsub", "adsub", "stbus", "adbus", "adbod"]:
                pos_list = Position.objects.filter(category=pos).order_by("sort")

                if pos_list.exists():
                    sections.append({
                        "title": pos_list.first().get_category_display(),
                        "positions": list(pos_list)
                    })

            return render(request, "teammanager/directory.html", {
                "sections": sections
            })

        else:
            return HttpResponseForbidden()


@csrf_exempt
def families(request):
    if request.method == 'GET' and not request.user.is_authenticated:
        return render(request, 'teammanager/family_login.html')
    else:
        if request.user.is_authenticated or request.POST.get("passcode", "none") == os.getenv("DIRECTORY_PASSCODE",
                                                                                              "1902"):
            fams = list(Family.objects.all().order_by("name"))
            singles = []

            for fam in list(fams):
                if fam.member_set.count() <= 1:
                    singles = singles + list(fam.member_set.all())
                    fams.remove(fam)

            return render(request, "teammanager/families.html", {
                "families": fams,
                "singles": singles,
            })
        else:
            return HttpResponseForbidden()
