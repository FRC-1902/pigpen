from django.urls import path

from .views import checkin_api

urls = [
    path('api/getstudents', checkin_api.get_members, name="api_members"),
    path('api/punch', checkin_api.punch, name="api_punch"),
]
