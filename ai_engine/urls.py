from django.urls import path
from .views import retrain_ai

urlpatterns = [
    path('retrain/', retrain_ai, name='retrain_ai'),
]