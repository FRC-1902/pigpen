from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from ..models import Member, Meeting, Punch, Token


def get_members(request):
    members = Member.objects.all()
    out = []

    for member in members:
        out.append({
            "id": member.id,
            "name": str(member),
            "position": member.role
        })

    return JsonResponse({"members": out})


@csrf_exempt
def do_punch(request):
    timezone.activate(settings.TIME_ZONE)

    if request.method == 'POST':
        data = request.POST
        if "secret" in data and "member" in data:
            # Authenticate against token in database
            if not Token.objects.filter(token=data['secret']).exists():
                return HttpResponseForbidden

            q = Member.objects.filter(id=data['member'])
            if q.exists():
                member = q.first()
                meeting = Meeting.objects.get_or_create(date=timezone.now().date())[0]

                pq = Punch.objects.filter(member=member, meeting=meeting, end=None)
                exists = pq.exists()
                if exists:
                    pun = pq.first()
                    pun.end = timezone.now()
                    pun.save()
                else:
                    pun = Punch(member=member, meeting=meeting)
                    pun.start = timezone.now()
                    pun.save()

                pun.refresh_from_db()  # Needed to fix naive datetime issue

                out = {
                    "success": True,
                    "member": str(member),
                }

                if not exists:
                    out.update({
                        "punch": "in",
                        "time": timezone.localtime(pun.start).strftime("%-I:%M %p")
                    })
                else:
                    out.update({
                        "punch": "out",
                        "time": timezone.localtime(pun.end).strftime("%-I:%M %p"),
                        "duration": str(pun.duration()).split('.')[0]
                    })

                return JsonResponse(out)

            else:
                return JsonResponse({
                    "success": False,
                    "error": "Member does not exist."
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


@csrf_exempt
def add_member(request):
    if request.method == 'POST':
        data = request.POST
        if 'secret' in data and 'first' in data and 'last' in data and 'role' in data:
            # Authenticate against token in database
            if not Token.objects.filter(token=data['secret']).exists():
                return HttpResponseForbidden

            m, created = Member.objects.get_or_create(first=data['first'], last=data['last'])

            if data['role'] in Member.roles:
                m.role = m

            m.save()

            return JsonResponse({
                "success": True,
                "created": created
            })

    return HttpResponseBadRequest()
