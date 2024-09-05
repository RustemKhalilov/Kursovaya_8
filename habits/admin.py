from django.contrib import admin
from habits.models import Habits


@admin.register(Habits)
class HabitsAdmin(admin.ModelAdmin):
    list_display = ["pk", "owner", "place", "time", "action"]
