from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .services import run_ai_analysis


@staff_member_required
def retrain_ai(request):
    run_ai_analysis()
    return HttpResponse("AI retraining completed successfully.")

from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin_view(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        return HttpResponse("Admin created")
    return HttpResponse("Admin already exists")
