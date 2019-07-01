from django.urls import path

from .views import checkin_api

urls = [
    path('api/getmembers', checkin_api.get_members, name="api_members"),
    path('api/punch', checkin_api.do_punch, name="api_punch"),
    path('api/gethours', checkin_api.get_hours, name="api_hours"),
]
