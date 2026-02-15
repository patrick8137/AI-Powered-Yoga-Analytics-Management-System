from django.urls import path
from .views import home
from .views import submit_contact

urlpatterns = [
    path('', home, name='home'),
    path('submit_contact/', submit_contact, name='submit_contact'),
]
