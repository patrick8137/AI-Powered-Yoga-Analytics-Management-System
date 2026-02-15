from django.contrib import admin
from .models import StudentProfile, MonthlyFee, FeeSetting

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'age',
        'phone',
        'progress_score',
        'ai_status',
        'created_at',
    )
    search_fields = ('user__username', 'user__email')
    list_filter = ('ai_status',)
    ordering = ('-created_at',)

@admin.register(MonthlyFee)
class MonthlyFeeAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'month',
        'amount',
        'is_paid',
        'paid_at',
    )
    list_filter = ('is_paid', 'month')
    search_fields = ('student__user__username',)
    ordering = ('-month',)
    actions = ['mark_selected_as_paid']

    def mark_selected_as_paid(self, request, queryset):
        for fee in queryset:
            if not fee.is_paid:
                fee.mark_as_paid()

    mark_selected_as_paid.short_description = "✅ Mark selected fees as PAID"

@admin.register(FeeSetting)
class FeeSettingAdmin(admin.ModelAdmin):
    list_display = ('monthly_fee_amount', 'updated_at')

    def has_add_permission(self, request):
        return not FeeSetting.objects.exists()
