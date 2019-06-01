from django.db import models


class Member(models.Model):
    roles = (
        ("stu", "Student"),
        ("mtr", "Mentor"),
        ("vol", "Volunteer")
    )

    first = models.TextField()
    last = models.TextField()
    role = models.CharField(max_length=10, default="stu", choices=roles)
    avatar = models.ImageField()


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
    signup_active = models.BooleanField()
    self_register = models.BooleanField()


class Punch(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()


class Registration(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    approved = models.BooleanField()
    notes = models.TextField(null=True, blank=True)
