from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'year',
        'created_at',
        'is_published',
    )

    list_filter = (
        'year',
        'is_published',
    )

    search_fields = (
        'title',
        'description',
    )

    ordering = ('-year',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations du projet', {
            'fields': (
                'title',
                'description',
                'year',
                'image',
            )
        }),
        ('Publication', {
            'fields': (
                'is_published',
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )
