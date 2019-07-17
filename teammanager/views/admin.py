from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect

from ..models import Member


def upload_photo(request):
    if request.method == "GET":
        return render(request, 'teammanager/upload_photo.html', {
            "members": Member.objects.all().order_by("first", "last")
        })
    else:
        post = request.POST
        files = list(request.FILES.keys())
        if 'member' in request.POST and 'photo' in request.FILES:
            m = Member.objects.get(id=request.POST['member'])
            m.avatar = request.FILES['photo']
            m.save()

            return redirect('man:admin_add_photo')
        else:
            return HttpResponseBadRequest()
