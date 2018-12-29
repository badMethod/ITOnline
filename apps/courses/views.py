from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Courses


# Create your views here.

class CoursesListView(View):
    def get(self, request):
        all_course = Courses.objects.all().order_by("-add_time")
        hot_course = Courses.objects.all().order_by("-click_nums")[:3]

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_course = all_course.order_by("-students")
            elif sort == "hot":
                all_course = all_course.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course, 6, request=request)

        all_course = p.page(page)
        return render(request, "course-list.html", {"all_course": all_course, "hot_course": hot_course, "sort": sort})
