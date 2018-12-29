from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from users.models import UserProfile, EmailVerityRecord
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetUserForm
from utils.email_send import send_register_email


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


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
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"message": "账号未激活"})
            else:
                return render(request, "login.html", {"message": "密码错误或账号不存在"})
        else:
            return render(request, "login.html", {"login_form": login_form})


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
