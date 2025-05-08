from django.contrib import admin

from habit_tracker.models import Habit


# Register your models here.
@admin.register(Habit)
class Habit(admin.ModelAdmin):
    list_display = ("time_action", "action", "nice", "period")
    search_fields = (
        "time_action",
        "action",
        "nice",
    )
