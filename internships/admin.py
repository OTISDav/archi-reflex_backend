from django.contrib import admin
from django.utils.html import format_html
from .models import Internship


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'school',
        'status',
        'created_at',
        'cv_link',
        'letter_link',
    )

    list_filter = ('status', 'school', 'created_at')
    search_fields = ('name', 'email', 'school', 'phone')

    ordering = ('-created_at',)

    list_editable = ('status',)

    readonly_fields = (
        'cv',
        'letter',
        'created_at',
    )

    # Liens CV
    def cv_link(self, obj):
        if obj.cv:
            url = obj.cv.url if hasattr(obj.cv, 'url') else obj.cv
            return format_html('<a href="{}" target="_blank">Voir CV</a>', url)
        return "-"
    cv_link.short_description = "CV"

    # Liens Lettre
    def letter_link(self, obj):
        if obj.letter:
            url = obj.letter.url if hasattr(obj.letter, 'url') else obj.letter
            return format_html('<a href="{}" target="_blank">Voir Lettre</a>', url)
        return "-"
    letter_link.short_description = "Lettre"
