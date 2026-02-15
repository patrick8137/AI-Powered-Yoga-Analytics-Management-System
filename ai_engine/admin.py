from django.contrib import admin
from .models import AIInsight
from .services import run_ai_analysis


@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ('student', 'cluster', 'updated_at')
    readonly_fields = ('student', 'cluster', 'message', 'updated_at')
    actions = ['retrain_ai']

    def retrain_ai(self, request, queryset):
        run_ai_analysis()
        self.message_user(request, "✅ AI retrained successfully.")

    retrain_ai.short_description = "🔁 Retrain AI Model"
