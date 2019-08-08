from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from teammanager.models import Member, Token, Punch, Meeting


def get_members(request):
    members = Member.objects.all().order_by("first")
    out = []
    members_in = [x.member for x in Punch.objects.filter(end__isnull=True)]

    for member in members:
        out.append({
            "id": member.id,
            "name": str(member),
            "position": member.role,
            "active": member.active,
            "isIn": bool(member in members_in)
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


def get_hours(request, member):
    if request.method == 'GET':
        try:
            hours = Member.objects.get(id=member).get_hours()

            # Coerce all values to string
            return JsonResponse(dict((k, str(v).split('.')[0]) for k, v in hours.items()))
        except Exception:
            pass

    return HttpResponseBadRequest()


def get_signed_in(request, member):
    if request.method == 'GET':
        member = Member.objects.get(id=member)

        # TODO: Fix meeting date late at night.
        meeting = Meeting.objects.filter(type='build', date=timezone.now().date())

        pq = Punch.objects.filter(member=member, end=None)
        if pq.exists():
            return JsonResponse({
                "signed_in": True
            })

        return JsonResponse({
            "signed_in": False
        })

    return HttpResponseBadRequest()
