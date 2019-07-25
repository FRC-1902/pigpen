from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect


def login(request):
    if request.method == 'POST':
        data = request.POST
        if 'username' in data and 'password' in data:
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                dj_login(request, user)

            return redirect('man:index')

    return HttpResponseBadRequest()


def logout(request):
    dj_logout(request)
    request.session.flush()
    return redirect('man:index')
