from django.urls import path

from .views.api import members, punch

urls = [
    path('api/getmembers', members.get_members, name="api_members"),
    path('api/gethours', members.get_hours, name="api_hours"),
    path('api/addmember', members.add_member, name="api_hours"),

    path('api/punch', punch.do_punch, name="api_punch"),
]
