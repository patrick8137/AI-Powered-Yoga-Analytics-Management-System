from django.contrib import admin
from .models import (
    InstructorProfile,
    InstructorStudent,
    Attendance,
    PracticeLog,
    LearningDocument
)

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'phone'
    )

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    full_name.short_description = 'Full Name'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

@admin.register(InstructorStudent)
class InstructorStudentAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'student')
    search_fields = ('instructor__user__username', 'student__user__username')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present')
    list_filter = ('date', 'present')
    search_fields = ('student__user__username',)


@admin.register(PracticeLog)
class PracticeLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'hours')
    list_filter = ('date',)
    search_fields = ('student__user__username',)


@admin.register(LearningDocument)
class LearningDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('title', 'instructor__user__username')
