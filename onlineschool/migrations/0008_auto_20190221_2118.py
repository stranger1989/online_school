# Generated by Django 2.1.5 on 2019-02-21 12:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineschool', '0007_auto_20190219_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonrecord',
            name='lesson_hour',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='受講時間'),
        ),
    ]
