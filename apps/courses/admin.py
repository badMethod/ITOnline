from django.contrib import admin
from courses.models import Courses, CoursesResource, Lesson, Video


# Register your models here.

class CoursesAdmin(admin.ModelAdmin):
    list_display = ["courseOrg", "name", "desc", "detail", "level", "learn_time", "students",
                    "fav_nums", "click_nums", "add_time"]


admin.site.register(Courses, CoursesAdmin)
admin.site.register(CoursesResource)
admin.site.register(Lesson)
admin.site.register(Video)
