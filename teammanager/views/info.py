from django.shortcuts import render


def registration_info(request):
    return render(request, "teammanager/info_registration.html")


def links(request):
    return render(request, "teammanager/info_links.html")
