from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from teammanager.models import Member, Punch, Meeting
import requests
import json


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

            response = {}
        if action_val:
            if action_val == "outreach_signup_create": # Picking an outreach signup to post
                response = {
                    "response_type": "ephemeral",
                    "blocks": outreach_create_blocks(posting="signup")
                }
            elif action_val == "outreach_checkin_create": # Picking an outreach checkin to post
                response = {
                    "response_type": "ephemeral",
                    "blocks": outreach_create_blocks(posting="checkin")
                }
            elif action_val.startswith("outreach_signup_create_"): # Posting an outreach signup
                meeting_id = int(action_val.replace("outreach_signup_create_", ""))
                response = {
                    "response_type": "in_channel",
                    "replace_original": False,
                    "text": "Lets sign up for meeting #{}!\n...once the feature is done.".format(meeting_id)
                }
            elif action_val.startswith("outreach_checkin_create_"): # Posting an outreach checkin
                meeting_id = int(action_val.replace("outreach_checkin_create_", ""))
                requests.post(response_url, json=response)
                response = {
                    "response_type": "in_channel",
                    "replace_original": False,
                    "blocks": outreach_checkin_blocks(Meeting.objects.get(id=meeting_id))
                }
            elif action_val.startswith("outreach_signup_"): # Signing up for an outreach
                meeting_id = int(action_val.replace("outreach_signup_", ""))
                response = {
                    "response_type": "ephemeral",
                    "replace_original": False,
                    "text": "Okay, you've signed up for meeting #{}!".format(meeting_id)
                }
            elif action_val.startswith("outreach_checkin_"):  # Checking in to an outreach
                meeting_id = int(action_val.replace("outreach_checkin_", ""))
                meeting = Meeting.objects.get(id=meeting_id)
                slack_id = data["user"]["id"]
                try:
                    member = Member.objects.get(slack=slack_id)
                except:
                    requests.post(response_url, json={
                        "text": "Could not find a Pigpen account associated with your Slack ID {}. Contact Ryan S. for help.".format(slack_id)
                    })
                    return HttpResponse(status=200)
                try:
                    punches = Punch.objects.filter(member=member, meeting=meeting)
                    for punch in punches:
                        if punch.is_complete():
                            requests.post(response_url, json={
                                "text": "You're currently punched in for this outreach already. Try punching out?"
                            })
                            return HttpResponse(status=200)
                except:
                    pass
                pun = Punch(member=member, meeting=meeting)
                pun.start = timezone.now()
                pun.save()
                response = {
                    "response_type": "ephemeral",
                    "replace_original": False,
                    "text": "Okay, you've checked in for {}!".format(meeting)
                }
            else:
                response = {
                    "response_type": "ephemeral",
                    "text": 'Unknown action "{}". Sorry! :sadparrot:'.format(action_val),
                    "emoji": True
                }
        else:
            response = {
                "text": "Encountered an error.\n{}".format(str(data))
            }
        requests.post(response_url, json=response)

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


def outreach_create_blocks(posting="signup"):
    options = []
    for meeting in Meeting.objects.all():
        options.append({
            "text": {
                "type": "plain_text",
                "text": str(meeting),
                "emoji": True
            },
            "value": "outreach_{}_create_{}".format(posting, meeting.id)
        })
    response = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Which outreach are we posting a {} for?".format(posting)
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


def outreach_checkin_blocks(meeting):
    response = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Check-in to outreach event *{}* opened! Make sure to click the button only once you've "
                        "arrived to the event.".format(meeting)
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "style": "primary",
                    "text": {
                        "type": "plain_text",
                        "text": ":wilbur: CHECK IN :wilbur:",
                        "emoji": True
                    },
                    "value": "outreach_checkin_{}".format(meeting.id)
                }
            ]
        }
    ]
    return response
