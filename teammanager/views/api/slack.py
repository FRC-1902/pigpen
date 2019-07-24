from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


@csrf_exempt
def action(request):
    if request.method == 'POST':
        data = request.POST["payload"]
        try:
            action_val = data["actions"][0]["value"]
        except Exception as e:
            print(e)
            print(data)
            return HttpResponse("rip")
        response_url = data["response_url"]
        if action_val == "outreach_signup_create":
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