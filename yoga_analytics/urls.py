from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend landing
    path('', include('frontend.urls')),

    # Auth
    path('accounts/', include('accounts.urls')),

    # Dashboards
    path('student/', include('students.urls')),
    path('instructor/', include('instructors.urls')),

    # AI
    path('ai/', include('ai_engine.urls')),

    # yoga_analytics/urls.py
    path('messages/', include('messaging.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
