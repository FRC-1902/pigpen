import os

from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..models import Family


@csrf_exempt
def families(request):
    if request.method == 'GET':
        return render(request, 'teammanager/families_login.html')
    else:
        if request.POST.get("passcode", "none") == os.getenv("DIRECTORY_PASSCODE", "1902"):
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
