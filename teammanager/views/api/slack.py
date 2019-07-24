from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


@csrf_exempt
def action(request):
    if request.POST:
        data = request.POST
        action = data["actions"][0]["value"]
        response_url = data["response_url"]
        if action == "outreach_signup_create":
            requests.post(response_url, json={
                "text": "It's 80 degrees right now."
            })

    return HttpResponse(status=200)


@csrf_exempt
def outreach(request):
    return JsonResponse(
        {
            "response-type": "ephemeral",
            "blocks": [
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
                            "value": "outreach_signup_create"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Outreach Check-In",
                                "emoji": True
                            },
                            "value": "outreach_checkin_create"
                        }
                    ]
                }
            ]})