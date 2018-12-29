from django.contrib import admin
from operation.models import CourseComments, UserAsk, UserCourse, UserFavorite, UserMessage

# Register your models here.
admin.site.register(CourseComments)
admin.site.register(UserAsk)
admin.site.register(UserCourse)
admin.site.register(UserFavorite)
admin.site.register(UserMessage)
