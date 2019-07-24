from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def action(request):
    return HttpResponse(status=200)


@csrf_exempt
def outreach(request):
    return HttpResponse(status=200)
