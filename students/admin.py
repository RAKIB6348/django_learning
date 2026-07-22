from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'roll_number', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'roll_number')
    list_filter = ('is_active',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'image')
        }),
        ('Academic Info', {
            'fields': ('roll_number', 'is_active')
        }),
        ('Parent Details', {
            'fields': ('father_name', 'mother_name', 'parent_phone', 'parent_email', 'parent_address')
        }),
    )


admin.site.register(Student, StudentAdmin)
