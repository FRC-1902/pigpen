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
                meeting = Meeting.objects.get_or_create(type='build', date=timezone.localdate())[0]

                if not member.active:
                    member.active = True
                    member.save()

                pq = Punch.objects.filter(member=member, meeting=meeting, end=None)
                exists = pq.exists()
                if exists:  # Punch out
                    pun = pq.first()

                    if (timezone.now() - pun.start).seconds < 120:
                        return JsonResponse({
                            "success": False,
                            "error": "You punched in too recently. Please wait at least 2 minutes before punching out."
                        })
                    else:
                        pun.end = timezone.now()
                        pun.save()
                else:  # Punch in
                    recent_pq = Punch.objects.filter(member=member, meeting=meeting,
                                                     end__gte=timezone.now() - timezone.timedelta(minutes=2))

                    if recent_pq.exists():
                        return JsonResponse({
                            "success": False,
                            "error": "You punched out too recently. Please wait at least 2 minutes before punching in."
                        })
                    else:
                        pun = Punch(member=member, meeting=meeting)
                        pun.start = timezone.now()

                        if data.get("temperature"):
                            pun.temperature = data['temperature']

                        pun.save()
                        meeting.members.add(member)

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
