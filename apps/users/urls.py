from django.urls import path, re_path
from .views import UserCentInfoView, UploadImageView, ChangePwdView, ChangeEmailView, MyCourseView, MyFavCourseView, \
    MyFavOrgView, MyFavTeacherView, MessageView

app_name = 'user_cent'

urlpatterns = [
    path("info/", UserCentInfoView.as_view(), name="info"),
    path("upload/", UploadImageView.as_view(), name="upload"),
    path("change_pwd/", ChangePwdView.as_view(), name="change_pwd"),
    path("sendemail_code/", ChangeEmailView.as_view(), name="sendemail_code"),
    path("my_course/", MyCourseView.as_view(), name="my_course"),
    path("my_fav_course/", MyFavCourseView.as_view(), name="my_fav_course"),
    path("my_fav_org/", MyFavOrgView.as_view(), name="my_fav_org"),
    path("my_fav_teacher/", MyFavTeacherView.as_view(), name="my_fav_teacher"),
    path("message/", MessageView.as_view(), name="message"),
]
