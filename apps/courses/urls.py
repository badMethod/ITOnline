from django.urls import path, re_path

from .views import CoursesListView, CourseDetailView, LessonDetailView, CommentDetailView, AddCommentView

app_name = 'courses'

urlpatterns = [
    path('list/', CoursesListView.as_view(), name="list"),
    path('add_comment/', AddCommentView.as_view(), name="add_comment"),
    re_path('detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
    re_path('lesson/(?P<course_id>\d+)/$', LessonDetailView.as_view(), name="lesson"),
    re_path('comment/(?P<course_id>\d+)/$', CommentDetailView.as_view(), name="comment"),
]


