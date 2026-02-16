from django.urls import path
from .views import retrain_ai

urlpatterns = [
    path('retrain/', retrain_ai, name='retrain_ai'),
]
from .views import create_admin_view

urlpatterns += [
    path('create-admin/', create_admin_view),
]
