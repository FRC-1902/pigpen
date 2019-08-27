from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models

from .utils import gen_token


class Token(models.Model):
    token = models.CharField(max_length=100, default=gen_token)
    comment = models.TextField()

    def __str__(self):
        return self.comment


class Family(models.Model):
    name = models.TextField()

    def __str__(self):
        return "The %s Family" % self.name


class Member(models.Model):
    roles = (
        ("stu", "Student"),
        ("mtr", "Adult"),
        ("asib", "Sibling"),
        ("vip", "VIP Bacon")
    )

    first = models.TextField()
    last = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=10, default="stu", choices=roles)
    active = models.BooleanField(default=True, null=False, blank=False)
    avatar = models.ImageField(null=True, blank=True)
    family = models.ForeignKey("Family", null=True, blank=True, on_delete=models.SET_NULL)
    hours = models.IntegerField(default=0, blank=False)
    outreach_hours = models.IntegerField(default=0, blank=False)
    attendance = models.IntegerField(default=0, blank=False)
    slack = models.CharField(max_length=20, null=True, blank=True)
    slack_username = models.CharField(max_length=50, null=True, blank=True)
    slack_avatar = models.TextField(null=True, blank=True)
    subtitle = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.first, self.last)

    def short_name(self):
        if not "-" in self.last:
            return "%s %s." % (self.first, self.last[0])
        else:
            parts = self.last.split("-")
            return "%s %s.%s." % (self.first, parts[0][0], parts[1][0])

    def get_hours(self):
        hours = {}
        hours['total'] = timedelta()
        hours['build'] = timedelta()
        hours['out'] = timedelta()
        for punch in Punch.objects.filter(member=self):
            if punch.is_complete() and bool(punch.meeting.type in ['build', 'out', 'othr']):
                if punch.meeting.type in ['build', 'othr']:
                    hours['build'] += punch.duration()
                    hours['total'] += punch.duration()
                elif punch.meeting.type in ['out']:
                    hours['out'] += punch.duration()
                    hours['total'] += punch.duration()

        return hours

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        elif self.slack_avatar:
            return self.slack_avatar
        else:
            return "http://pen.explodingbacon.com/static/teammanager/no_profile.png"


class Position(models.Model):
    categories = [
        ("stoff", "Student Officers"),
        ("tmldr", "Team Leadership"),
        ("adbod", "Adult Board of Directors"),
        ("stsub", "Student Subsystem/Subteam Leads"),
        ("adsub", "Adult Subsystem/Subteam Leads"),
        ("stbus", "Student Business Leads"),
        ("adbus", "Adult Business Leads"),
        ("old", "People to Know")
    ]

    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    name = models.TextField()
    category = models.CharField(max_length=10, choices=categories)
    sort = models.IntegerField(default=50)

    def __str__(self):
        return "%s (%s)" % (self.name, str(self.member))


class Meeting(models.Model):
    types = (
        ("build", "Build Meeting"),  # Official open time, counts toward hours and total open time
        ("out", "Outreach"),  # Official outreach, that counts toward outreach hours
        ("comp", "Competition"),  # Competition, does not count toward hours or total open time
        ("fun", "Fun Event"),  # Does not count towards hours or total open time
        ("othr", "Other Non-Mandatory")  # Counts hours, but does not count towards total open time
    )

    date = models.DateField()
    type = models.CharField(max_length=10, default="build", choices=types)
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    length = models.IntegerField(null=False, default=4)
    signup_active = models.BooleanField(default=False)
    signup_notes_needed = models.BooleanField(default=False)
    members = models.ManyToManyField("Member", blank=True)
    verified = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        if self.name:
            return "%s on %s" % (self.name, self.date)
        else:
            return "%s on %s" % (self.get_type_display(), self.date)

    def get_name(self):
        if self.name:
            return self.name
        else:
            return self.get_type_display()

    def hours_sum(self, member):
        sum = None
        punches = Punch.objects.filter(member=member, meeting=self)

        for punch in punches:
            if punch.is_complete():
                if not sum:
                    sum = timedelta()
                sum = sum + punch.duration()

        return sum

class Punch(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    fake = models.BooleanField(default=False)

    def duration(self):
        return self.end - self.start

    def is_complete(self):
        return bool(self.meeting) and bool(self.start) and bool(self.end)

    def __str__(self):
        return "%s punched at %s" % (str(self.member), str(self.meeting))


class Registration(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    approved = models.BooleanField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s registered at %s" % (str(self.member), str(self.meeting))


class TeambuildingQuestion(models.Model):
    question = models.TextField(null=True, blank=True)
    option_one = models.CharField(max_length=100, null=False, blank=False)
    option_two = models.CharField(max_length=100, null=False, blank=False)
    active = models.BooleanField(default=False)
    used = models.BooleanField(default=False)

    def __str__(self):
        if self.question:
            return self.question
        else:
            return "%s or %s" % (self.option_one, self.option_two)


class TeambuildingResponse(models.Model):
    question = models.ForeignKey("TeambuildingQuestion", on_delete=models.CASCADE)
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    option_one_selected = models.BooleanField(default=False)
    option_two_selected = models.BooleanField(default=False)

    def __str__(self):
        return "%s responded to %s" % (str(self.member), str(self.question))
