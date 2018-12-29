from django.contrib import admin
from users.models import UserProfile, EmailVerityRecord, Banner


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "nickname", "email", "is_active", "is_staff", "is_superuser", "phone", "last_login",
                    "date_joined"]


class EmailVerityRecordAdmin(admin.ModelAdmin):
    list_display = ["code", "email", "send_type", "send_time"]


class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "image", "url", "index", "add_time"]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerityRecord, EmailVerityRecordAdmin)
admin.site.register(Banner, BannerAdmin)
