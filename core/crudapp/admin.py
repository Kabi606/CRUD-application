from django.contrib import admin
from . models import Aiquest


@admin.register(Aiquest)
class AiquestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'teacher_name', 'course_name', 'course_duration', 'seat'
    ]

