from django.contrib import admin
from .models import Appointment
from core.emails import send_notification
from core.google_calendar import create_calendar_event


@admin.action(description="Marquer comme confirmé")
def mark_confirmed(modeladmin, request, queryset):
    for appointment in queryset:
        if appointment.status == "accepted":
            continue

        appointment.status = "accepted"

        # Google Calendar
        try:
            event_id = create_calendar_event(appointment)
            appointment.google_event_id = event_id
        except Exception as e:
            modeladmin.message_user(
                request,
                f"Erreur Google Calendar pour {appointment.name} : {e}",
                level="error"
            )

        appointment.save()

        # Email client
        send_notification(
            "Rendez-vous confirmé",
            f"Bonjour {appointment.name},\nVotre rendez-vous est confirmé.",
            appointment.email
        )


@admin.action(description="Marquer comme refusé")
def mark_rejected(modeladmin, request, queryset):
    for appointment in queryset:
        if appointment.status == "rejected":
            continue

        appointment.status = "rejected"
        appointment.save()

        # Email client
        send_notification(
            "Rendez-vous refusé",
            f"Bonjour {appointment.name},\nVotre rendez-vous a été refusé.",
            appointment.email
        )


@admin.action(description="Marquer comme en attente")
def mark_pending(modeladmin, request, queryset):
    queryset.update(status="pending")


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

    readonly_fields = (
        "status",
        "google_event_id",
        "created_at",
    )

    actions = (
        mark_confirmed,
        mark_rejected,
        mark_pending,
    )

    fieldsets = (
        ("Client", {
            "fields": ("name", "email", "phone"),
        }),
        ("Rendez-vous", {
            "fields": ("project_type", "date", "time"),
        }),
        ("Google Calendar", {
            "fields": ("google_event_id",),
        }),
        ("Meta", {
            "fields": ("created_at",),
        }),
    )
