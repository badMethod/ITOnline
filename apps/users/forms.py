from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, min_length=3)


class RegisterForm(forms.Form):
    email = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, min_length=3)
    captcha = CaptchaField()


class ForgetPwdForm(forms.Form):
    email = forms.CharField(required=True, min_length=3)
    captcha = CaptchaField()


class ResetUserForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=3)
    password2 = forms.CharField(required=True, min_length=3)
