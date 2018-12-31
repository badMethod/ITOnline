from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from organization.models import CityDict, CourseOrg, Teacher
from operation.models import UserFavorite
from .forms import UserAskForm
from courses.models import Courses


# Create your views here.
class OrgListView(View):
    def get(self, request):
        all_citys = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        hot_org = all_orgs.order_by("-students")[0:3]

        keywords = request.GET.get("keywords", "")
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        city_id = request.GET.get('city', "")
        courseType = request.GET.get('ct', "")
        sort = request.GET.get('sort', "")
        if city_id:
            all_orgs = all_orgs.filter(cityDict_id=int(city_id))
        if courseType:
            all_orgs = all_orgs.filter(courseType=courseType)

        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 10, request=request)

        orgs = p.page(page)

        orgs_count = all_orgs.count()
        return render(request, "org-list.html",
                      {"all_citys": all_citys, "all_orgs": orgs, "orgs_count": orgs_count, "hot_org": hot_org,
                       "city_id": city_id, "courseType": courseType, "sort": sort, "students": sort, "courses": sort})


class UserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg": "请检查重新填写"}', content_type="application/json")


class OrgDetailHomeView(View):
    def get(self, request, org_id):
        active = "home"
        courseOrg = CourseOrg.objects.get(id=org_id)
        courseOrg.click_nums += 1
        courseOrg.save()
        all_courses = courseOrg.courses_set.all().order_by("-students")[:4]
        all_teachers = courseOrg.teacher_set.all().order_by("-click_nums")[:2]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_id=org_id, fav_type=2, user=request.user):
                has_fav = True
        return render(request, "org-detail-homepage.html",
                      {"courseOrg": courseOrg, "all_course": all_courses, "all_teacher": all_teachers,
                       "active": active, "has_fav": has_fav})


class OrgDetailCourseView(View):
    def get(self, request, org_id):
        active = "course"
        courseOrg = CourseOrg.objects.get(id=org_id)
        all_courses = courseOrg.courses_set.all().order_by("-students")
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_id=org_id, fav_type=2, user=request.user):
                has_fav = True
        return render(request, "org-detail-course.html",
                      {"courseOrg": courseOrg, "all_course": all_courses, "active": active, "has_fav": has_fav})


class OrgDetailDescView(View):
    def get(self, request, org_id):
        active = "desc"
        courseOrg = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_id=org_id, fav_type=2, user=request.user):
                has_fav = True
        return render(request, "org-detail-desc.html",
                      {"courseOrg": courseOrg, "active": active, "has_fav": has_fav})


class OrgDetailTeacherView(View):
    def get(self, request, org_id):
        active = "teacher"
        courseOrg = CourseOrg.objects.get(id=org_id)
        all_teachers = courseOrg.teacher_set.all().order_by("-click_nums")
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_id=org_id, fav_type=2, user=request.user):
                has_fav = True
        return render(request, "org-detail-teachers.html",
                      {"courseOrg": courseOrg, "all_teacher": all_teachers,
                       "active": active, "has_fav": has_fav})


class UserFavoriteView(View):
    def post(self, request):
        if request.user.is_authenticated:
            fav_id = request.POST.get("fav_id", 0)
            fav_type = request.POST.get("fav_type", 0)
            user_favs = UserFavorite.objects.filter(fav_id=fav_id, fav_type=fav_type, user_id=request.user.id)
            if user_favs:
                user_favs.delete()
                if fav_type == "1":
                    course = Courses.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif fav_type == "2":
                    courseOrg = CourseOrg.objects.get(id=int(fav_id))
                    courseOrg.fav_nums -= 1
                    if courseOrg.fav_nums < 0:
                        courseOrg.fav_nums = 0
                    courseOrg.save()
                elif fav_type == "3":
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            else:
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav = UserFavorite()
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.user = request.user
                    user_fav.save()
                    if fav_type == "1":
                        course = Courses.objects.get(id=int(fav_id))
                        course.fav_nums += 1
                        course.save()
                    elif fav_type == "2":
                        courseOrg = CourseOrg.objects.get(id=int(fav_id))
                        courseOrg.fav_nums += 1
                        courseOrg.save()
                    elif fav_type == "3":
                        teacher = Teacher.objects.get(id=int(fav_id))
                        teacher.fav_nums += 1
                        teacher.save()
                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()
        rank_teacher = all_teacher.order_by("-click_nums")[:5]
        count = all_teacher.count()

        keywords = request.GET.get("keywords", "")
        if keywords:
            all_teacher = all_teacher.filter(
                Q(name__icontains=keywords) | Q(work_position__icontains=keywords) | Q(points__icontains=keywords))

        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teacher = all_teacher.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teacher, 2, request=request)

        all_teacher = p.page(page)

        return render(request, "teachers-list.html",
                      {"all_teacher": all_teacher, "rank_teacher": rank_teacher, "count": count, "sort": sort})


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        courses = teacher.courses_set.all()
        rank_teacher = Teacher.objects.all().order_by("-click_nums")[:5]
        has_teacher_fav = False
        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
            has_teacher_fav = True
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.courseOrg_id, fav_type=2):
            has_org_fav = True
        return render(request, "teacher-detail.html",
                      {"teacher": teacher, "courses": courses, "rank_teacher": rank_teacher,
                       "has_teacher_fav": has_teacher_fav, "has_org_fav": has_org_fav})
