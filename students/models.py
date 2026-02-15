from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    progress_score = models.FloatField(default=0)
    ai_status = models.CharField(max_length=50, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class FeeSetting(models.Model):
    monthly_fee_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=1000
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Monthly Fee = ₹{self.monthly_fee_amount}"

class MonthlyFee(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='monthly_fees'
    )

    month = models.DateField(
        help_text="Use the first day of the month (e.g. 2026-02-01)"
    )

    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'month')
        ordering = ['-month']

    def mark_as_paid(self):
        self.is_paid = True
        self.paid_at = now()
        self.save()

    def __str__(self):
        status = "Paid" if self.is_paid else "Pending"
        return f"{self.student.user.username} - {self.month.strftime('%B %Y')} ({status})"
