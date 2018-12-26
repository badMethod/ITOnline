from django.db import models


# Create your models here.

class Courses(models.Model):
    name = models.CharField(max_length=30, verbose_name="课程名")
    desc = models.CharField(max_length=200, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    level = models.CharField(max_length=10, choices=(("easy", "初级"), ("normal", "中级"), ("hard", "高级")),
                             verbose_name="课程等级")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长（min）")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    courses = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="章节名")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="视频名")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name


class CoursesResource(models.Model):
    courses = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="资源名称")
    download = models.FileField(upload_to="courses/resource/%Y/%m", verbose_name="下载地址")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
