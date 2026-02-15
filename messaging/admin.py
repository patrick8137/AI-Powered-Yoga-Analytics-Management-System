from django.contrib import admin
from .models import Message, BroadcastMessage


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'short_content', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'content')

    def short_content(self, obj):
        return obj.content[:40]
    
@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'created_at')
    search_fields = ('content',)