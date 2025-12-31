from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project_type',
        'year',
        'created_at',
    )

    list_filter = (
        'project_type',
        'year',
    )

    search_fields = (
        'title',
        'description',
    )

    ordering = ('-year',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Informations du projet', {
            'fields': (
                'title',
                'description',
                'project_type',
                'year',
                'image',
            )
        }),
        ('Date de création', {
            'fields': (
                'created_at',
            )
        }),
    )
