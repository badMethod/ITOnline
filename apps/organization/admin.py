from django.contrib import admin
from organization.models import CityDict, CourseOrg, Teacher


# Register your models here.

class CityDictAdmin(admin.ModelAdmin):
    list_display = ["name", "desc", "add_time"]


class CourseOrgAdmin(admin.ModelAdmin):
    list_display = ["cityDict", "name", "courseType", "desc", "students", "course_nums", "click_nums", "fav_nums",
                    "image", "address", "add_time"]


class TeacherAdmin(admin.ModelAdmin):
    list_display = ["courseOrg", "name", "work_years", "work_company", "work_position", "points", "click_nums",
                    "fav_nums", "add_time"]


admin.site.register(CityDict, CityDictAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)
