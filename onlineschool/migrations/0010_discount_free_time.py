# Generated by Django 2.1.5 on 2019-02-24 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineschool', '0009_auto_20190222_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='free_time',
            field=models.IntegerField(default=0, verbose_name='無料時間'),
        ),
    ]
