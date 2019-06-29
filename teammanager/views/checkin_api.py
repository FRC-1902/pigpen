from datetime import datetime

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
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
def punch(request):
    if request.method == 'POST':
        data = request.POST
        if "secret" in data and "member" in data:
            # Authenticate against token in database
            if not Token.objects.filter(token=data['token']).exists():
                return HttpResponseForbidden

            q = Member.objects.filter(id=data['member'])
            if q.exists():
                member = q.first()
                meeting = Meeting.objects.get_or_create(date=datetime.now().date())[0]

                pq = Punch.objects.filter(member=member, meeting=meeting, end=None)
                exists = pq.exists()
                if exists:
                    pun = pq.first()
                    pun.end = datetime.now()
                    pun.save()
                else:
                    pun = Punch(member=member, meeting=meeting)
                    pun.start = datetime.now()
                    pun.save()

                return JsonResponse({
                    "success": True,
                    "member": str(member),
                    "punch": "Out" if exists else "In"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Member does not exist."
                })

    return HttpResponseBadRequest()
