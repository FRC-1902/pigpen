from django.http.response import HttpResponse


def action(request):
    return HttpResponse(status=200)


def outreach(request):
    return HttpResponse(status=200)
