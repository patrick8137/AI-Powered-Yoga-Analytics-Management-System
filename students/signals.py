from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timezone import now

from .models import StudentProfile, MonthlyFee, FeeSetting


def get_month_start(dt=None):
    if not dt:
        dt = now().date()
    return dt.replace(day=1)

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=StudentProfile)
def create_initial_monthly_fee(sender, instance, created, **kwargs):
    if not created:
        return

    month_start = get_month_start()

    fee_setting = FeeSetting.objects.first()
    amount = fee_setting.monthly_fee_amount if fee_setting else 1000

    MonthlyFee.objects.get_or_create(
        student=instance,
        month=month_start,
        defaults={'amount': amount}
    )


def ensure_current_month_fee(student):
    month_start = get_month_start()

    fee_setting = FeeSetting.objects.first()
    amount = fee_setting.monthly_fee_amount if fee_setting else 1000

    MonthlyFee.objects.get_or_create(
        student=student,
        month=month_start,
        defaults={'amount': amount}
    )
