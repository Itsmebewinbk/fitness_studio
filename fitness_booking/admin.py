from django.contrib import admin
from .models import FitnessClass, Booking


@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "instructor",
        "datetime",
        "total_slots",
        "available_slots",
        "is_deleted",
    )
    list_filter = (
        "instructor",
        "datetime",
        "is_deleted",
    )
    search_fields = ("name", "instructor")
    ordering = ("-datetime",)
    date_hierarchy = "datetime"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "client_email",
        "fitness_class",
        "created_at",
    )
    list_filter = ("fitness_class",)
    search_fields = (
        "client_name",
        "client_email",
        "fitness_class__name",
    )
    ordering = ("-created_at",)
