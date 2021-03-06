from django.db import models
from organization.models import CourseOrg, Teacher


# Create your models here.

class Courses(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=Teacher, blank=Teacher, verbose_name="所属讲师")
    courseOrg = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    name = models.CharField(max_length=30, verbose_name="课程名")
    desc = models.CharField(max_length=200, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    level = models.CharField(max_length=10, choices=(("easy", "初级"), ("normal", "中级"), ("hard", "高级")),
                             verbose_name="课程等级")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长（min）")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    type = models.CharField(max_length=20, default="", verbose_name="课程类型")
    tag = models.CharField(max_length=20, default="", verbose_name="课程标签")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    you_need = models.CharField(max_length=100, verbose_name="须知", default="")
    you_get = models.CharField(max_length=100, verbose_name="你能学到的", default="")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()


class Lesson(models.Model):
    courses = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="章节名")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="视频名")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CoursesResource(models.Model):
    courses = models.ForeignKey(Courses, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="资源名称")
    download = models.FileField(upload_to="courses/resource/%Y/%m", verbose_name="下载地址")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
