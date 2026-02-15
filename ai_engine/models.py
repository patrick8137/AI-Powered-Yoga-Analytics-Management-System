from django.db import models
from students.models import StudentProfile


class AIInsight(models.Model):
    student = models.OneToOneField(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='ai_insight'
    )
    cluster = models.IntegerField(default=0)
    status = models.CharField(
        max_length=50,
        default="Analysis Pending"
    )
    message = models.TextField(
        default="AI analysis pending. More data required."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.status}"
