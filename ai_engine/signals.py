from django.db.models.signals import post_save
from django.dispatch import receiver

from students.models import StudentProfile
from instructors.models import Attendance, PracticeLog
from .models import AIInsight
from .services import run_ai_analysis

@receiver(post_save, sender=StudentProfile)
def create_ai_insight(sender, instance, created, **kwargs):
    if created:
        AIInsight.objects.get_or_create(
            student=instance,
            defaults={
                'cluster': 0,
                'message': "AI analysis pending. Collecting initial data."
            }
        )

@receiver(post_save, sender=Attendance)
@receiver(post_save, sender=PracticeLog)
def retrain_ai_on_activity_change(sender, instance, created, **kwargs):
    if created:
        run_ai_analysis()
