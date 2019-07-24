from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from teammanager.models import Meeting


@csrf_exempt
def action(request):
    if request.method == 'POST':
        data = json.loads(request.POST["payload"])
        response_url = data["response_url"]
        action_val = None
        if "value" in data["actions"][0]:
            action_val = data["actions"][0]["value"]
        elif "selected_option" in data["actions"][0]:
            action_val = data["actions"][0]["selected_option"]["value"]

        if action_val:
            if action_val == "outreach_signup_create":
                requests.post(response_url, json={
                    "blocks": outreach_blocks(posting="signup")
                })
            elif action_val == "outreach_checkin_create":
                requests.post(response_url, json={
                    "blocks": outreach_blocks(posting="checkin")
                })
            elif action_val == "post_signup": # TODO: remove
                requests.post(response_url, json={
                    "text": str(data)
                })
            elif action_val.startswith("signup_meeting_"):
                meeting_id = int(action_val.replace("signup_meeting_", ""))
                requests.post(response_url, json={
                    "text": "Wooo lets sign up for meeting #{}!".format(meeting_id)
                })
            else:
                requests.post(response_url, json={
                    "text": 'Unknown action "{}". Sorry! :sadparrot:'.format(action_val),
                    "emoji": True
                })
        else:
            requests.post(response_url, json={
                "text": "Encountered an error.\n{}".format(str(data))
            })

    return HttpResponse(status=200)


@csrf_exempt
def outreach(request):
    #return JsonResponse(outreach_blocks(), safe=False)
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


def outreach_blocks(posting="signup"):
    options = []
    for meeting in Meeting.objects.all():
        options.append({
            "text": {
                "type": "plain_text",
                "text": str(meeting),
                "emoji": True
            },
            "value": "{}_meeting_{}".format(posting, meeting.id)
        })
    response = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Which outreach are we posting for?"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": True
                },
                "options": options
            }
        }
    ]

    return response
