from django.db import models

from .utils import gen_token


class Token(models.Model):
    token = models.CharField(max_length=100, default=gen_token)
    comment = models.TextField()

    def __str__(self):
        return self.comment


class Member(models.Model):
    roles = (
        ("stu", "Student"),
        ("mtr", "Mentor"),
        ("vol", "Volunteer")
    )

    first = models.TextField()
    last = models.TextField()
    role = models.CharField(max_length=10, default="stu", choices=roles)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.first, self.last)


class Meeting(models.Model):
    types = (
        ("build", "Build Meeting"),
        ("out", "Outreach"),
        ("comp", "Competition"),
        ("fun", "Fun Event"),
        ("othr", "Other Mandatory")
    )

    date = models.DateField()
    type = models.CharField(max_length=10, default="build", choices=types)
    name = models.TextField(null=True, blank=True)
    signup_active = models.BooleanField(default=False)
    self_register = models.BooleanField(default=False)

    def __str__(self):
        return "%s on %s" % (self.get_type_display(), self.date)


class Punch(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def duration(self):
        return self.end - self.start

    def __str__(self):
        return "%s punched at %s" % (str(self.member), str(self.meeting))


class Registration(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    approved = models.BooleanField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s registered at %s" % (str(self.member), str(self.meeting))
