import os
import re
from datetime import timedelta

import pytz
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from teammanager.models import Punch, Member, Family, Meeting, TeambuildingQuestion


def close_old_punches():
    tz = pytz.timezone("America/New_York")
    yesterday = timezone.now().astimezone(tz).replace(hour=4, minute=0, second=0)
    q = Punch.objects.filter(end__isnull=True, start__lt=yesterday)

    for p in q:
        if p.meeting.type == 'build':
            if p.start.weekday() > 4:  # Weekends
                p.end = p.start.astimezone(tz).replace(hour=17, minute=0, second=0)
            else:  # Weekdays
                p.end = p.start.astimezone(tz).replace(hour=21, minute=0, second=0)

            if p.start < p.end:  # Sanity check
                p.save()
            else:  # Discard punches in after meeting end if not manually punched out.
                pass  # Actually, do nothing (for now).


def create_families():
    for member in Member.objects.filter(family__isnull=True):
        fq = Family.objects.filter(name=member.last)

        if fq.exists():
            member.family = fq.first()
        else:
            f = Family(name=member.last)
            f.save()
            member.family = f

        member.save()

    for fam in Family.objects.all():
        if not fam.member_set.exists():
            fam.delete()


def add_members_to_build_meetings():
    for meeting in Meeting.objects.exclude(type="out"):
        for punch in Punch.objects.filter(meeting=meeting):
            meeting.members.add(punch.member)


def update_hours():
    for member in Member.objects.all():
        pq = Punch.objects.filter(member=member)
        hours = timedelta()
        outreach_hours = timedelta()

        for punch in pq:
            if punch.is_complete() and bool(punch.meeting.type in ['build', 'othr']):
                hours += punch.duration()

            if punch.is_complete() and bool(punch.meeting.type in ['out']):
                outreach_hours += punch.duration()

        member.hours = hours.total_seconds()
        member.outreach_hours = outreach_hours.total_seconds()

        member.save()


def mark_users_inactive():
    for member in Member.objects.filter(role="mtr"):
        try:
            if timezone.now() - timedelta(days=100) > member.punch_set.exclude(end__isnull=True).order_by("-end").first().end:
                member.active = False
                member.save()
        except AttributeError as e:
            member.active = False
            member.save()


def get_slack_users():
    key = os.getenv("SLACK_OAUTH")

    if key is not None:
        resp = requests.get("https://slack.com/api/users.list?token=" + key)

        for member in resp.json().get("members", []):
            # print(member)
            try:
                profile = member.get("profile", {})
                name = profile.get("real_name")
                first = str(name.split(" ")[0])
                last = str(name.split(" ")[-1])

                mq = Member.objects.filter(slack=member.get("id"))

                if not mq.exists():
                    mq = Member.objects.filter(first__iexact=first, last__iexact=last)

                if mq.exists():
                    m = mq.first()
                    m.subtitle = re.sub(r":\w*:", "", profile.get("status_text", None)).strip()
                    m.slack = member.get("id")
                    m.slack_avatar = profile.get("image_512")

                    if bool(profile.get("display_name_normalized")):
                        m.slack_username = profile.get("display_name_normalized")
                    else:
                        m.slack_username = profile.get("real_name_normalized")

                    m.save()
                else:
                    print("Can't find " + first + " " + last)
            except Exception as e:
                print(e)

    else:
        print("NO KEY")


def mark_teambuilding_questions_used():
    for q in TeambuildingQuestion.objects.filter(used=False):
        if q.response_set.exists():
            q.used = True
            q.save()


class Command(BaseCommand):
    def handle(self, **options):
        close_old_punches()
        create_families()
        add_members_to_build_meetings()
        update_hours()
        mark_users_inactive()
        get_slack_users()  # Also gets subtitles
        mark_teambuilding_questions_used()
