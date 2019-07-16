from django.urls import path

from .views import index, auth, hours, facebook
from .views.api import members, punch

app_name = "teammanager"
urlpatterns = [
    path('', index.index, name="index"),
    path('hours', hours.hours, name="hours"),
    path('hours/table', hours.hours_table, name="hours_table"),
    path('hours/outreach/add', hours.outreach_hours_add, name="outreach_hours_add"),

    path('facebook', facebook.families, name="families"),

    path('location', index.location, name="location"),

    path('login', auth.login, name="login"),
    path('logout', auth.logout, name="logout"),

    path('api/members/add', members.add_member, name="api_hours"),
    path('api/members/all', members.get_members, name="api_members"),
    path('api/member/<int:member>/hours', members.get_hours, name="api_hours"),
    path('api/member/<int:member>/signedin', members.get_signed_in, name="api_hours"),

    path('api/punch', punch.do_punch, name="api_punch"),
]
