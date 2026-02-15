from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import ContactMessage

@require_POST
def submit_contact(request):
    ContactMessage.objects.create(
        name=request.POST.get('name'),
        email=request.POST.get('email'),
        message=request.POST.get('message'),
    )
    return redirect('/')


def home(request):
    return render(request, 'frontend/home.html')