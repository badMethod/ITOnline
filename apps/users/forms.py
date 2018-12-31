from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile
import re

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


class ImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["picture"]


class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nickname", "birthday", "gender", "address", "phone"]

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
