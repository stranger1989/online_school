# Generated by Django 2.1.5 on 2019-02-22 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onlineschool', '0008_auto_20190221_2118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limited_hour', models.IntegerField(verbose_name='閾時間')),
                ('discount_price', models.IntegerField(verbose_name='割引額')),
                ('lesson_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineschool.Lesson', verbose_name='ジャンル名')),
            ],
            options={
                'db_table': 'discount',
            },
        ),
        migrations.AlterField(
            model_name='lessonrecord',
            name='lesson_hour',
            field=models.IntegerField(verbose_name='受講時間'),
        ),
    ]