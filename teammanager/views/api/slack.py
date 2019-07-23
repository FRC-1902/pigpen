from django.http.response import HttpResponse, JsonResponse


def action(request):
    return HttpResponse(status=200)


def outreach(request):
    return JsonResponse({
        "text": "Command received."
    })
