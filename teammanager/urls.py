from django.urls import path

from .views import index, auth
from .views.api import members, punch

app_name = "teammanager"
urlpatterns = [
    path('', index.index, name="index"),

    path('login', auth.login, name="login"),
    path('logout', auth.logout, name="logout"),

    path('api/members/add', members.add_member, name="api_hours"),
    path('api/members/all', members.get_members, name="api_members"),
    path('api/member/<int:member>/hours', members.get_hours, name="api_hours"),
    path('api/member/<int:member>/signedin', members.get_signed_in, name="api_hours"),

    path('api/punch', punch.do_punch, name="api_punch"),
]
