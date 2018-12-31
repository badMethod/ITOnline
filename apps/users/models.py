from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=20, verbose_name="nickname")
    birthday = models.DateField(verbose_name="birthday", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="male",
                              verbose_name="gender")
    address = models.CharField(max_length=100, default="", verbose_name="address")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="phone")
    picture = models.ImageField(upload_to="image/%Y/%m", default="image/default", max_length=200,
                                verbose_name="picture")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.username}---{self.email}"

    def get_unread_message(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerityRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=30, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回账号"), ("change", "修改邮箱")),
                                 default="register", max_length=30)
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.email}---{self.code}"


class Banner(models.Model):
    title = models.CharField(max_length=30, verbose_name="标题")
    image = models.ImageField(max_length=100, upload_to="banner/%Y/%m", verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
