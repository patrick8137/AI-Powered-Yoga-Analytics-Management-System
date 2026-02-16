from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .services import run_ai_analysis


@staff_member_required
def retrain_ai(request):
    run_ai_analysis()
    return HttpResponse("AI retraining completed successfully.")

