from django.http.response import HttpResponse, JsonResponse


def action(request):
    return HttpResponse(status=200)


def outreach(request):
    return JsonResponse([
    {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "Welcome to the Outreach Manager! What would you like to post?",
            "emoji": True
        }
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Outreach Signup",
                    "emoji": True
                },
                "value": "signup"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Outreach Check-In",
                    "emoji": True
                },
                "value": "checkin"
            }
        ]
    }
])
