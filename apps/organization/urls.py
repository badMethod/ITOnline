from django.urls import path, re_path

from .views import OrgListView, UserAskView, OrgDetailHomeView, OrgDetailCourseView, OrgDetailDescView, \
    OrgDetailTeacherView, UserFavoriteView, TeacherListView, TeacherDetailView

app_name = 'org'

urlpatterns = [
    path('list/', OrgListView.as_view(), name="org_list"),
    path('add_ask/', UserAskView.as_view(), name="add_ask"),
    re_path('detail_home/(?P<org_id>\d+)/$', OrgDetailHomeView.as_view(), name="detail_home"),
    re_path('detail_course/(?P<org_id>\d+)/$', OrgDetailCourseView.as_view(), name="detail_course"),
    re_path('detail_desc/(?P<org_id>\d+)/$', OrgDetailDescView.as_view(), name="detail_desc"),
    re_path('detail_teacher/(?P<org_id>\d+)/$', OrgDetailTeacherView.as_view(), name="detail_teacher"),
    path('add_fav/', UserFavoriteView.as_view(), name="add_fav"),
    path('teacher_list/', TeacherListView.as_view(), name="teacher_list"),
    re_path('teacher_detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
