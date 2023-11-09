from django.contrib import admin

from .models import Student, University


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'surname',
        'father_name',
        'entrance_year',
        'university'
    )


admin.site.register(Student, StudentAdmin)


class UniversityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'short_name',
        'foundation_date'
    )


admin.site.register(University, UniversityAdmin)
