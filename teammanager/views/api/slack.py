from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json


@csrf_exempt
def action(request):
    if request.method == 'POST':
        data = json.loads(request.POST["payload"])
        print(data)
        response_url = data["response_url"]
        action_val = None
        for act in data["actions"]:
            if "value" in act:
                action_val = act
                break
        if action_val and action_val == "outreach_signup_create":
            requests.post(response_url, json={
                "payload": {
                    "text": "You clicked outreach signup create! Hurray!"
                }
            })
        else:
            requests.post(response_url, json={
                "payload": {
                    "text": "Unknown action. Sorry! :("
                }
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
                                "text": "Post a Signup",
                                "emoji": True
                            },
                            "value": "outreach_signup_create"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Post a Check-In",
                                "emoji": True
                            },
                            "value": "outreach_checkin_create"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Create an Outreach",
                                "emoji": True
                            },
                            "value": "outreach_create"
                        },
                    ]
                }
            ]})