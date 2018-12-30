from django.db import models


# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name="城市名称")
    desc = models.CharField(max_length=200, verbose_name="城市描述")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    cityDict = models.ForeignKey(CityDict, verbose_name="所在城市", on_delete=models.CASCADE)
    courseType = models.CharField(max_length=20, default="training",
                                  choices=(("training", "培训机构"), ("university", "高校"), ("personal", "个人")),
                                  verbose_name="机构类型")
    name = models.CharField(max_length=30, verbose_name="机构名称")
    desc = models.CharField(max_length=30, verbose_name="机构描述")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图")
    address = models.CharField(max_length=50, verbose_name="机构地址")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_course_nums(self):
        return self.courses_set.all().count()


class Teacher(models.Model):
    courseOrg = models.ForeignKey(CourseOrg, verbose_name="所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="头像", default="")

    class Meta:
        verbose_name = "任课老师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
