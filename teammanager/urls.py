from django.urls import path

from .views import index, auth, hours, directory, attendance, admin, outreach
from .views.api import members, punch, slack, slack_oauth

app_name = "teammanager"
urlpatterns = [
    path('', index.index, name="index"),
    path('hours', hours.hours, name="hours"),
    path('hours/table', hours.hours_table, name="hours_table"),
    path('hours/outreach/add', hours.outreach_hours_add, name="outreach_hours_add"),
    path('hours/groups', hours.attendance_groups, name="hours_groups"),

    path('directory', directory.directory, name="directory_all"),
    path('directory/leaders', directory.leaders, name="directory_leaders"),
    path('directory/families', directory.families, name="directory_families"),
    path('directory/staff', directory.staff_list, name="directory_staff"),

    path('outreach/fromcal', outreach.create_outreach_from_calendar, name="outreach_from_calendar"),

    path('location', attendance.whos_in, name="location"),

    path('meetings/', attendance.meetings, name="meetings"),
    path('meetings/<int:id>', attendance.meeting_breakdown, name="meeting"),
    path('meetings/verify', attendance.meetings_verify, name="meetings_verify"),

    path('member/<int:id>', attendance.member, name="member"),
    path("members/noslack", attendance.no_slack_list, name="no_slack"),

    path('login', auth.login, name="login"),
    path('logout', auth.logout, name="logout"),
    path('auth/slack/login', slack_oauth.slack_login, name="slack_oauth_login"),

    path('admin/addphoto', admin.upload_photo, name="admin_add_photo"),

    path('api/members/add', members.add_member, name="api_hours"),
    path('api/members/all', members.get_members, name="api_members"),
    path('api/member/<int:member>/hours', members.get_hours, name="api_hours"),
    path('api/member/<int:member>/signedin', members.get_signed_in, name="api_hours"),

    path('api/punch', punch.do_punch, name="api_punch"),

    path('api/slack/action', slack.action, name="slack_action"),
    path('api/slack/outreach', slack.outreach, name="slack_outreach"),
]
