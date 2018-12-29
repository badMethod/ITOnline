from django.urls import path, re_path

from .views import CoursesListView

urlpatterns = [
    path('list/', CoursesListView.as_view(), name="list"),
]
