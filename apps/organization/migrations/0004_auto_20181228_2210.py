# Generated by Django 2.1.4 on 2018-12-28 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_courseorg_coursetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='course_num',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=0, verbose_name='学习人数'),
        ),
    ]
