from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from teammanager.models import TeambuildingQuestion


def add_question(request):
    if request.method == 'GET':
        return render(request, 'teammanager/teambuilding_question_add.html')
    else:
        data = request.POST
        print(data)
        if 'option_one' in data and 'option_two' in data:
            tq, created = TeambuildingQuestion.objects.get_or_create(
                question=data.get("question"),
                option_one=data.get("option_one"),
                option_two=data.get("option_two")
            )

            tq.save()

            return render(request, 'teammanager/teambuilding_question_add.html', {"success": tq})

        return HttpResponse(status=400)


@staff_member_required
def select_question(request):
    if request.method == 'GET':
        return render(request, 'teammanager/teambuilding_question_select.html', {
            "current_question": TeambuildingQuestion.objects.filter(active=True).first(),
            "questions": TeambuildingQuestion.objects.all()
        })
    else:
        data = request.POST
        if 'question_id' in data:
            new_q = TeambuildingQuestion.objects.get(id=data['question_id'])

            for q in TeambuildingQuestion.objects.filter(active=False):
                q.active = False
                q.save()

            new_q.active = True
            new_q.save()

        return redirect('man:teambuilding_select')
