# Generated by Django 2.1.5 on 2019-02-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineschool', '0004_auto_20190219_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonrecord',
            name='lesson_date',
            field=models.DateField(verbose_name='受講日'),
        ),
    ]