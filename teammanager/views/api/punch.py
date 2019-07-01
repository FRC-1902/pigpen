from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from teammanager.models import Token, Member, Meeting, Punch


@csrf_exempt
def do_punch(request):
    timezone.activate(settings.TIME_ZONE)

    if request.method == 'POST':
        data = request.POST
        if "secret" in data and "member" in data:
            # Authenticate against token in database
            if not Token.objects.filter(token=data['secret']).exists():
                return HttpResponseForbidden()

            q = Member.objects.filter(id=data['member'])
            if q.exists():
                member = q.first()
                meeting = Meeting.objects.get_or_create(type='build', date=timezone.now().date())[0]

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
