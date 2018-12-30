from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Courses
from operation.models import UserCourse, UserFavorite, CourseComments
from utils.mixin import LoginRequiredMixin


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


class CourseDetailView(View):

    def get(self, request, course_id):
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            user_fav_course = UserFavorite.objects.filter(user=request.user, fav_type=1)
            if user_fav_course:
                has_fav_course = True
        if request.user.is_authenticated:
            user_fav_org = UserFavorite.objects.filter(user=request.user, fav_type=2)
            if user_fav_org:
                has_fav_org = True
        course = Courses.objects.get(id=course_id)
        relate_course = Courses.objects.filter(tag=course.tag).exclude(id=course_id).order_by("-click_nums")[:1]
        user_course = UserCourse.objects.filter(course_id=course_id)
        return render(request, "course-detail.html",
                      {"course": course, "relate_course": relate_course, "user_course": user_course,
                       "has_fav_course": has_fav_course, "has_fav_org": has_fav_org, "course_id": course_id})


class LessonDetailView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = 'next'

    def get(self, request, course_id):
        course = Courses.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse()
            user_course.course_id = course_id
            user_course.user_id = request.user.id
            user_course.save()

        all_user = UserCourse.objects.filter(course=course)
        user_ids = [user.user_id for user in all_user]
        all_course = UserCourse.objects.filter(user_id__in=user_ids)
        c_ids = [c.course_id for c in all_course]
        relate_course = Courses.objects.filter(id__in=c_ids)[:3]
        return render(request, "course-video.html",
                      {"course_id": course_id, "course": course, "relate_course": relate_course})


class CommentDetailView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = 'next'

    def get(self, request, course_id):
        course = Courses.objects.get(id=course_id)

        all_user = UserCourse.objects.filter(course=course)
        user_ids = [user.user_id for user in all_user]
        all_course = UserCourse.objects.filter(user_id__in=user_ids)
        c_ids = [c.course_id for c in all_course]
        relate_course = Courses.objects.filter(id__in=c_ids)[:3]

        comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        return render(request, "course-comment.html",
                      {"course_id": course_id, "course": course, "relate_course": relate_course, "comments": comments})


class AddCommentView(View):
    # login_url = "/login/"
    # redirect_field_name = 'next'

    def post(self, request):
        if request.user.is_authenticated:
            course_id = request.POST.get("course_id", 0)
            comments = request.POST.get("comments", "")
            comment = CourseComments()
            comment.user = request.user
            comment.course_id = course_id
            comment.comment = comments
            comment.save()
            return HttpResponse('{"status":"success", "msg":"发表成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
