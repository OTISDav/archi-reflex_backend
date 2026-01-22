from django.contrib import admin
from .models import Appointment

@admin.action(description="Marquer comme confirmé")
def mark_confirmed(modeladmin, request, queryset):
    queryset.update(status=Appointment.Status.accepted)


@admin.action(description="Marquer comme annulé")
def mark_cancelled(modeladmin, request, queryset):
    queryset.update(status=Appointment.Status.rejected)


@admin.action(description="Marquer comme en attente")
def mark_pending(modeladmin, request, queryset):
    queryset.update(status=Appointment.Status.PENDING)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "project_type",
        "status",
        "date",
        "created_at",
    )
    list_filter = (
        "status",
        "project_type",
        "date",
        "created_at",
    )
    search_fields = (
        "name",
        "email",
        "phone",
        "project_type",
    )
    ordering = ("-created_at",)
    readonly_fields = ("google_event_id", "created_at")
    actions = [mark_confirmed, mark_cancelled, mark_pending]

    fieldsets = (
        ("Client", {
            "fields": ("name", "email", "phone"),
        }),
        ("Rendez-vous", {
            "fields": ("project_type", "date", "status"),
        }),
        ("Google Calendar", {
            "fields": ("google_event_id",),
        }),
        ("Meta", {
            "fields": ("created_at",),
        }),
    )
