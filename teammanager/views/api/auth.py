from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from teammanager.models import Token


@csrf_exempt
def exchange_token(request):
    if request.method == "POST" and "key" in request.POST:
        key = request.POST['key']
        q = Token.objects.filter(exchanged=False, key=key)

        if q.exists():
            t = q.first()
            t.exchanged = True
            t.save()

            return JsonResponse({
                "success": True,
                "token": t.token
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "Token not found matching key given"
            })
    else:
        return HttpResponse(status=400)
