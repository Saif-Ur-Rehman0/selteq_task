from django.contrib import admin
from TaskApp.models import Task

class TaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)