from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from teammanager.models import Member, Token, Punch


def get_members(request):
    members = Member.objects.all().order_by("last")
    out = []

    for member in members:
        out.append({
            "id": member.id,
            "name": str(member),
            "position": member.role
        })

    return JsonResponse({"members": out})


@csrf_exempt
def add_member(request):
    if request.method == 'POST':
        data = request.POST
        if 'secret' in data and 'first' in data and 'last' in data and 'role' in data:
            # Authenticate against token in database
            if not Token.objects.filter(token=data['secret']).exists():
                return HttpResponseForbidden()

            m, created = Member.objects.get_or_create(first=data['first'], last=data['last'])

            if any(data['role'] in r for r in Member.roles):
                m.role = data['role']

            m.save()

            return JsonResponse({
                "success": True,
                "created": created
            })

    return HttpResponseBadRequest()


def get_hours(request):
    if request.method == 'GET':
        data = request.GET
        if 'member' in data:
            hours = {}
            for punch in Punch.objects.filter(member__id=data['member']):
                if punch.is_complete():
                    if punch.meeting.type in hours:
                        hours[punch.meeting.type] += punch.duration()
                    else:
                        hours[punch.meeting.type] = punch.duration()

            # Coerce all values to string
            return JsonResponse(dict((k, str(v).split('.')[0]) for k, v in hours.items()))

    return HttpResponseBadRequest()
