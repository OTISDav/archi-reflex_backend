from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'year',
        'created_at',
    )

    list_filter = (
        'year',
    )

    search_fields = (
        'title',
        'description',
    )

    ordering = ('-year',)

    readonly_fields = ('created_at',)  # ✅ updated_at supprimé

    fieldsets = (
        ('Informations du projet', {
            'fields': (
                'title',
                'description',
                'year',
                'image',
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
            )
        }),
    )
