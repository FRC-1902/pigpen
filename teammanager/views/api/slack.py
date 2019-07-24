from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def action(request):
    return HttpResponse(status=200)


@csrf_exempt
def outreach(request):
    return JsonResponse({
    "text": "It's 80 degrees right now.",
    "attachments": [
        {
            "text":"Partly cloudy today and tomorrow"
        }
    ]
})
