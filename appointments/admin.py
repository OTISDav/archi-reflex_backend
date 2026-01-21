from django.contrib import admin
from django.conf import settings
from .models import Appointment
from core.google_calendar import create_calendar_event
from core.emails import send_notification


# ==========================
# 🔹 Actions Admin
# ==========================
@admin.action(description="Marquer comme confirmé")
def mark_confirmed(modeladmin, request, queryset):
    for appointment in queryset:
        if appointment.status != Appointment.Status.CONFIRMED:
            appointment.status = Appointment.Status.CONFIRMED
            appointment.save()  # déclenche les signals et logique de sauvegarde

            # 🔹 Créer l'événement Google Calendar si pas déjà fait
            try:
                if not appointment.google_event_id:
                    event_id = create_calendar_event(appointment)
                    appointment.google_event_id = event_id
                    appointment.save()
            except Exception as e:
                print(f"Erreur Google Calendar action admin: {e}")

            # 🔹 Envoyer email au client
            try:
                send_notification(
                    subject="Votre rendez-vous est confirmé ✅",
                    message=(
                        f"Bonjour {appointment.name},\n\n"
                        f"Votre rendez-vous pour le projet '{appointment.project_type}' a été confirmé.\n"
                        f"📅 Date : {appointment.date}\n"
                        f"⏰ Heure : {appointment.time}\n\n"
                        "À très bientôt."
                    ),
                    recipient=appointment.email
                )
            except Exception as e:
                print(f"Erreur email confirmation action admin: {e}")


@admin.action(description="Marquer comme annulé")
def mark_cancelled(modeladmin, request, queryset):
    for appointment in queryset:
        if appointment.status != Appointment.Status.CANCELLED:
            appointment.status = Appointment.Status.CANCELLED
            appointment.save()

            # 🔹 Envoyer email au client
            try:
                send_notification(
                    subject="Rendez-vous annulé ❌",
                    message=(
                        f"Bonjour {appointment.name},\n\n"
                        f"Votre rendez-vous pour le projet '{appointment.project_type}' a été annulé."
                    ),
                    recipient=appointment.email
                )
            except Exception as e:
                print(f"Erreur email annulation action admin: {e}")


@admin.action(description="Marquer comme en attente")
def mark_pending(modeladmin, request, queryset):
    for appointment in queryset:
        appointment.status = Appointment.Status.PENDING
        appointment.save()


# ==========================
# 🔹 Admin Appointment
# ==========================
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
