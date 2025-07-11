from django.contrib import admin

from app_run.models import Run


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'created_at', 'comment')
    list_filter = ('status',)
