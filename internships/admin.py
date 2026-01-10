from django.contrib import admin
from .models import Internship
from django.utils.html import format_html

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'school', 'status', 'created_at', 'cv_link', 'letter_link')
    list_filter = ('status', 'school', 'created_at')
    search_fields = ('name', 'email', 'school', 'phone')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_editable = ('status',)  # Permet de changer le statut directement depuis la liste

    # Afficher les liens vers CV et lettre
    def cv_link(self, obj):
        if obj.cv:
            return format_html('<a href="{}" target="_blank">Voir CV</a>', obj.cv.url if hasattr(obj.cv, 'url') else obj.cv)
        return "-"
    cv_link.short_description = "CV"

    def letter_link(self, obj):
        if obj.letter:
            return format_html('<a href="{}" target="_blank">Voir Lettre</a>', obj.letter.url if hasattr(obj.letter, 'url') else obj.letter)
        return "-"
    letter_link.short_description = "Lettre"
