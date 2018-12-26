from users.models import UserProfile
from courses.models import Courses

from django.db import models


# Create your models here.

class UserAsk(models.Model):
    name = models.CharField(max_length=30, verbose_name="用户名")
    mobile = models.CharField(max_length=20, verbose_name="手机号")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户名", on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, verbose_name="课程名", on_delete=models.CASCADE)
    comment = models.CharField(max_length=300, verbose_name="评论")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户名", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.CharField(max_length=10, choices=((1, "课程"), (2, "课程机构"), (3, "课程讲师")), default=1,
                                verbose_name="收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接受用户")
    message = models.CharField(max_length=200, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户名", on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, verbose_name="课程名", on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户学习课程"
        verbose_name_plural = verbose_name
