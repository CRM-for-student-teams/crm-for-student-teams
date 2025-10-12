from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import Client, ClientStage, ActivityLog

class ActivityLogInline(admin.TabularInline):
    model = ActivityLog
    extra = 1  
    readonly_fields = ('inserted_at',)  

@admin.register(Client)
class ClientAdmin(BaseModelAdmin):
    list_display = ('fullname', 'email', 'phone_number', 'stage', 'team')
    list_filter = ('stage', 'team')
    search_fields = ('fullname', 'email')
    inlines = [ActivityLogInline]

@admin.register(ClientStage)
class ClientStageAdmin(BaseModelAdmin):
    list_display = ('status',)

@admin.register(ActivityLog)
class ActivityLogAdmin(BaseModelAdmin):
    list_display = ('user', 'client', 'action', 'inserted_at')
    list_filter = ('inserted_at', 'client', 'user')  
    search_fields = ('client__fullname', 'action', 'user__username')