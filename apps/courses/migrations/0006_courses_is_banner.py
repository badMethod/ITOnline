# Generated by Django 2.1.4 on 2019-01-01 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20181230_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
    ]
