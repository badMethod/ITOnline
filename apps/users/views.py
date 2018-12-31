from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from users.models import UserProfile, EmailVerityRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Courses
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetUserForm, ImageForm, UpdateInfoForm
from utils.email_send import send_register_email
from utils.mixin import LoginRequiredMixin
import json


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        banners = Banner.objects.all().order_by("-index")[:5]
        courses = Courses.objects.filter(is_banner=False).order_by("-click_nums")[:6]
        banner_courses = Courses.objects.filter(is_banner=True).order_by("-click_nums")[:2]
        orgs = CourseOrg.objects.all().order_by("-click_nums")[:15]
        return render(request, "index.html",
                      {"banners": banners, "courses": courses, "banner_courses": banner_courses, "orgs": orgs})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"message": "账号未激活"})
            else:
                return render(request, "login.html", {"message": "密码错误或账号不存在"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            if UserProfile.objects.get(email=email):
                return render(request, "register.html", {"register_form": register_form, "message": "账号已存在"})
            user = UserProfile()
            user.username = email
            user.nickname = email
            user.email = email
            user.password = make_password(password)
            user.is_active = False
            user.save()
            send_register_email(email, "register")
            message = UserMessage()
            message.user = request.user.id
            message.message = "欢迎注册慕课网！"
            message.has_read = False
            message.save()
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    def get(self, request, email_code):
        email_record = EmailVerityRecord.objects.filter(code=email_code)
        if email_record:
            for er in email_record:
                try:
                    user = UserProfile.objects.get(email=er.email)
                    user.is_active = True
                    user.save()
                except Exception as e:
                    return render(request, "login.html", {"message": "该账号状态异常，请联系管理员"})
                return render(request, "login.html", {"message": "激活成功，请登录"})
        else:
            return render(request, "login.html", {"message": "链接异常，请联系管理员"})


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            user = UserProfile.objects.filter(email=email)
            if user:
                send_register_email(email, "forget")
                message = UserMessage()
                message.user = request.user.id
                message.message = "您正在找回账号，如果是本人操作请忽略！"
                message.has_read = False
                message.save()
                return render(request, "forgetpwd.html", {"message": "找回邮件已发送，请查看邮箱", "forgetpwd_form": forgetpwd_form})
            else:
                return render(request, "forgetpwd.html", {"message": "账号不存在", "forgetpwd_form": forgetpwd_form})
        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})


class LinkResetUserView(View):
    def get(self, request, email_code):
        email_reset = EmailVerityRecord.objects.filter(code=email_code)
        if email_reset:
            for er in email_reset:
                email = er.email
                code = er.code
                return render(request, "password_reset.html", {"email": email, "code": code})
        else:
            return render(request, "forgetpwd.html", {"message": "链接异常，请联系管理员"})


class ResetUserView(View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        resetUser_form = ResetUserForm(request.POST)
        if resetUser_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 == password2:
                user = UserProfile.objects.get(email=email)
                if user:
                    user.password = make_password(password1)
                    user.save()
                    return render(request, "login.html", {"message": "密码修改成功，请登录"})
                else:
                    return render(request, "forgetpwd.html", {"message": "账号不存在"})
            else:
                return render(request, "password_reset.html",
                              {"resetUser_form": resetUser_form, "message": "两次输入的密码不同", "code": code, "email": email})
        else:
            return render(request, "password_reset.html",
                          {"resetUser_form": resetUser_form, "code": code, "email": email})

    def get(self, request):
        resetUser_form = ResetUserForm()
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        return render(request, "password_reset.html",
                      {"resetUser_form": resetUser_form, "code": code, "email": email})


class UserCentInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "usercenter-info.html", {})

    def post(self, request):
        info_form = UpdateInfoForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"请重新检查重新检查重新检查重新检查重新检查重新检查重新检查重新检查重新检查"}',
                                content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = ImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ChangePwdView(LoginRequiredMixin, View):
    def post(self, request):
        reset_form = ResetUserForm(request.POST)
        if reset_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 == password2:
                request.user.password = make_password(password1)
                request.user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class ChangeEmailView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get("email", "")
        if email:
            if not UserProfile.objects.filter(email=email):
                send_register_email(email, "change")
                return HttpResponse('{"status":"success"}', content_type='application/json')
            return HttpResponse('{"status":"exist"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        if EmailVerityRecord.objects.filter(email=email, code=code):
            request.user.email = email
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        all_user_course = UserCourse.objects.filter(user=request.user)
        courses = []
        for user_course in all_user_course:
            course = Courses.objects.get(id=user_course.course_id)
            courses.append(course)
        return render(request, "usercenter-mycourse.html", {"courses": courses})


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        all_user_fav = UserFavorite.objects.filter(user=request.user, fav_type=1)
        courses = []
        for user_fav in all_user_fav:
            course = Courses.objects.get(id=user_fav.fav_id)
            courses.append(course)
        return render(request, "usercenter-fav-course.html", {"courses": courses})


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        all_user_fav = UserFavorite.objects.filter(user=request.user, fav_type=2)
        orgs = []
        for user_fav in all_user_fav:
            org = CourseOrg.objects.get(id=user_fav.fav_id)
            orgs.append(org)
        return render(request, "usercenter-fav-org.html", {"orgs": orgs})


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        all_user_fav = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teachers = []
        for user_fav in all_user_fav:
            teacher = Teacher.objects.get(id=user_fav.fav_id)
            teachers.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {"teachers": teachers})


class MessageView(LoginRequiredMixin, View):
    def get(self, request):
        messages = UserMessage.objects.filter(user=request.user.id).order_by("-add_time")
        for message in messages:
            if not message.has_read:
                message.has_read = True
                message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(messages, 3, request=request)

        messages = p.page(page)
        return render(request, "usercenter-message.html", {"messages": messages})
