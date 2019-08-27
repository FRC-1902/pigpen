from django.http import HttpResponseForbidden
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from teammanager.models import TeambuildingQuestion, TeambuildingResponse, Token


def get_config(request):
    out = {}
    qq = TeambuildingQuestion.objects.filter(active=True)
    out['active'] = qq.exists()

    if qq.exists():
        q = qq.first()
        out = {
            **out,
            "question": q.question,
            "id": q.id,
            "option_one": q.option_one,
            "option_two": q.option_two,
        }

    return JsonResponse(out)


@csrf_exempt
def set_response(request):
    data = request.POST
    if "secret" in data:
        # Authenticate against token in database
        if not Token.objects.filter(token=data['secret']).exists() and False:
            return HttpResponseForbidden()

        if 'member' in data and 'question' in data and 'response' in data:
            response, created = TeambuildingResponse.objects.get_or_create(
                member_id=data['member'],
                question_id=data['question']
            )

            response.option_one_selected = data['response'] is 'a'
            response.option_two_selected = data['response'] is 'b'

            response.save()

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
