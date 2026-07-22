from django.contrib import admin
from .models import Class, Section, Subject


class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fieldsets = (
        ('Class Info', {
            'fields': ('name',)
        }),
    )


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_ref')
    search_fields = ('name', 'class_ref__name')
    list_filter = ('class_ref',)
    fieldsets = (
        ('Section Info', {
            'fields': ('name', 'class_ref')
        }),
    )


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'class_ref')
    search_fields = ('name', 'code', 'class_ref__name')
    list_filter = ('class_ref',)
    fieldsets = (
        ('Subject Info', {
            'fields': ('name', 'code', 'class_ref')
        }),
    )


admin.site.register(Class, ClassAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Subject, SubjectAdmin)
