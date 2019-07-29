from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse
from teammanager.models import Member, Punch, Meeting
from datetime import datetime
import requests
import json
import os


@csrf_exempt
def action(request):
    if request.method == 'POST':
        data = json.loads(request.POST["payload"])
        response_url = data["response_url"]
        action_val = None
        if "actions" in data:
            if "value" in data["actions"][0]:
                action_val = data["actions"][0]["value"]
            elif "selected_option" in data["actions"][0]:
                action_val = data["actions"][0]["selected_option"]["value"]
        elif data["type"] == "dialog_submission" or data["type"] == "dialog_cancellation":
            action_val = data["callback_id"]

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
                meeting = Meeting.objects.get(id=meeting_id)
                meeting.signup_active = True
                meeting.save()

                requests.post(response_url, json={
                    "text": "Alright! Posting..."
                })
                response = {
                    "response_type": "in_channel",
                    "replace_original": False,
                    "blocks": outreach_signup_blocks(meeting)
                }
            elif action_val.startswith("outreach_checkin_create_"): # Posting an outreach checkin
                meeting_id = int(action_val.replace("outreach_checkin_create_", ""))
                meeting = Meeting.objects.get(id=meeting_id)

                requests.post(response_url, json={
                    "text": "Alright! Posting..."
                })
                response = {
                    "response_type": "in_channel",
                    "replace_original": False,
                    "blocks": outreach_checkin_blocks(meeting)
                }

            elif action_val.startswith("outreach_signup_"): # Signing up for an outreach
                sumission = None
                if "submission" in data:
                    submission = data["submission"]
                    meeting_id = int(submission["state"])
                else:
                    meeting_id = int(action_val.replace("outreach_signup_", ""))
                meeting = Meeting.objects.get(id=meeting_id)
                slack_id = data["user"]["id"]
                try:
                    member = Member.objects.get(slack=slack_id)
                except:
                    requests.post(response_url, json={
                        "text": "Could not find a Pigpen account associated with your Slack ID {}. Contact Ryan or Dominic for help.".format(
                            slack_id)
                    })
                    return HttpResponse(status=200)

                if member in meeting.members.all():
                    response = {
                        "response_type": "ephemeral",
                        "replace_original": False,
                        "text": "You're already signed up for *{}*!".format(meeting)
                    }
                else:
                    if meeting.signup_notes_needed and not submission:
                        trigger_id = data["trigger_id"]
                        dialog = outreach_signup_notes_dialog(trigger_id, meeting)
                        res = requests.post("https://slack.com/api/dialog.open", json=dialog,
                                            headers={"Authorization": "Bearer {}".format(os.getenv("SLACK_OAUTH"))})
                        return HttpResponse(status=200)
                    else:
                        meeting.members.add(member)
                        meeting.save()
                        requests.post(response_url, json={
                            "blocks": outreach_signup_blocks(meeting)
                        })
                        response = {
                            "response_type": "ephemeral",
                            "replace_original": False,
                            "text": "Okay, you've signed up for *{}*.".format(meeting)
                        }
            elif action_val.startswith("outreach_checkin_"):  # Checking in to an outreach
                meeting_id = int(action_val.replace("outreach_checkin_", ""))
                meeting = Meeting.objects.get(id=meeting_id)
                slack_id = data["user"]["id"]
                try:
                    member = Member.objects.get(slack=slack_id)
                except:
                    requests.post(response_url, json={
                        "text": "Could not find a Pigpen account associated with your Slack ID {}. Contact Ryan or Dominic for help.".format(slack_id)
                    })
                    return HttpResponse(status=200)
                try:
                    punches = Punch.objects.filter(member=member, meeting=meeting)
                    for punch in punches:
                        if not punch.is_complete():
                            requests.post(response_url, json={
                                "response_type": "ephemeral",
                                "replace_original": False,
                                "text": "You're currently punched in for this outreach already. Try punching out?"
                            })
                            return HttpResponse(status=200)
                except:
                    pass
                pun = Punch(member=member, meeting=meeting)
                pun.start = timezone.now()
                pun.save()
                meeting.members.add(member)
                meeting.save()
                response = {
                    "response_type": "ephemeral",
                    "replace_original": False,
                    "blocks": outreach_checkout_blocks(meeting)
                }
            elif action_val.startswith("outreach_checkout_"):  # Checking OUT of an outreach
                meeting_id = int(action_val.replace("outreach_checkout_", ""))
                meeting = Meeting.objects.get(id=meeting_id)
                slack_id = data["user"]["id"]
                try:
                    member = Member.objects.get(slack=slack_id)
                except:
                    requests.post(response_url, json={
                    "text": "Could not find a Pigpen account associated with your Slack ID {}. Contact Ryan or Dominic for help.".format(
                        slack_id)
                    })
                    return HttpResponse(status=200)
                completed = False
                try:
                    punches = Punch.objects.filter(member=member, meeting=meeting)
                    for punch in punches:
                        if not punch.is_complete():
                            punch.end = timezone.now()
                            punch.save()
                            response = {
                                "text": "You've checked out of {}. Time: {}".format(meeting, punch.duration())
                            }
                            completed = True
                            break
                    if not completed:
                        response = {
                            "text": "I don't know how you pulled this off, but you weren't even checked in in the first place."
                        }
                except:
                    pass
            elif action_val.startswith("outreach_create"): # Pulling up the outreach creation dialog
                trigger_id = data["trigger_id"]
                dialog = outreach_create_dialog(trigger_id)
                res = requests.post("https://slack.com/api/dialog.open", json=dialog, headers={"Authorization": "Bearer {}".format(os.getenv("SLACK_OAUTH"))})
                response = {
                    "text": "Creating outreach..."
                }
            elif action_val == "outreach_new": # Creating an outreach
                submission = data["submission"]
                info = submission["signup_type"]
                signup_notes_needed = submission["signup_type"] == "info"

                try:
                    date = datetime.strptime(submission["date"], '%m-%d-%Y')
                except Exception as e:
                    requests.post(response_url, json={
                        "text": "Failed to parse date."
                    })
                    return HttpResponse(status=200)

                meeting = Meeting(type="out", name=submission["name"], date=date, signup_notes_needed=signup_notes_needed)
                meeting.save()
                response = {
                    "text": "Outreach *{}* created!".format(meeting)
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
    for meeting in Meeting.objects.filter(type="out"):
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
                "text": "Which outreach are we posting a {} for? Be careful, once you select an event I'll post the {} "
                        "for it *in this channel* immediately.".format(posting, posting)
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an Outreach",
                    "emoji": True
                },
                "options": options
            }
        }
    ]

    return response


def outreach_signup_blocks(meeting):
    text = "Sign-up for outreach event *{}*! Be sure you can attend before you click on the button. <http://pen.vegetarianbaconite.com{}|See the sign up list here!>".format(meeting, reverse("man:meeting", kwargs={"id": meeting.id}))
    member_count = len(meeting.members.all())
    if member_count > 0:
        if member_count == 1:
            text = text + "\n{} people is attending.".format(member_count)
        else:
            text = text + "\n{} people are attending.".format(member_count)
    response = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
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
                        "text": ":parrot: SIGN UP:parrot:",
                        "emoji": True
                    },
                    "value": "outreach_signup_{}".format(meeting.id)
                }
            ]
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


def outreach_checkout_blocks(meeting):
    response = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You've checked in to *{}*! Click the button below once you leave the event.".format(meeting)
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "style": "danger",
                    "text": {
                        "type": "plain_text",
                        "text": ":bacon: CHECK OUT :bacon:",
                        "emoji": True
                    },
                    "value": "outreach_checkout_{}".format(meeting.id)
                }
            ]
        }
    ]
    return response


def outreach_create_dialog(trigger_id):
    data = {
        "trigger_id": trigger_id,
        "dialog": {
            "callback_id": "outreach_new",
            "title": "Create an Outreach",
            "submit_label": "Create",
            "notify_on_cancel": True,
            "state": "Limo",
            "elements": [
                {
                    "type": "text",
                    "label": "Event Name",
                    "name": "name"
                },
                {
                    "type": "text",
                    "label": "Date (i.e. 4-20-2019)",
                    "name": "date"
                },
                {
                    "label": "Signup Type",
                    "type": "select",
                    "name": "signup_type",
                    "value": "one",
                    "options": [
                        {
                            "label": "One-Click Signup",
                            "value": "one"
                        },
                        {
                            "label": "Additional Info Needed",
                            "value": "info"
                        }
                    ]
                }
            ]
        }
    }
    return data


def outreach_signup_notes_dialog(trigger_id, outreach):
    data = {
        "trigger_id": trigger_id,
        "dialog": {
            "callback_id": "outreach_signup_notes",
            "title": "Sign up for Outreach",
            "submit_label": "Confirm",
            "notify_on_cancel": True,
            "state": "{}".format(outreach.id),
            "elements": [
                {
                    "label": "Additional Information",
                    "name": "info",
                    "type": "textarea",
                    "hint": "Additional information is required for signup. This might be what you're bringing, who's"
                            " driving you, etc..."
                }
            ]
        }
    }
    return data
