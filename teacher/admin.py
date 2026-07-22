from django.contrib import admin
from .models import Teacher


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'hire_date', 'is_active', 'user')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active',)
    readonly_fields = ('user',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'image')
        }),
        ('Employment Info', {
            'fields': ('hire_date', 'is_active')
        }),
        ('Linked User', {
            'fields': ('user',),
            'classes': ('collapse',),
        }),
    )


admin.site.register(Teacher, TeacherAdmin)
