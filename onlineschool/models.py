from django.db import models
from django.utils import timezone


class User(models.Model):
    SEX_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )

    class Meta:
        db_table = 'user'

    name = models.CharField(verbose_name='名前', max_length=255)
    sex = models.CharField(verbose_name='性別', max_length=255)
    age = models.IntegerField(verbose_name='年齢')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    class Meta:
        db_table = 'lesson'

    name = models.CharField(verbose_name='名前', max_length=255)
    basic_charge = models.IntegerField(verbose_name='基本料金')
    pay_per_charge = models.IntegerField(verbose_name='従量料金')

    def __str__(self):
        return self.name


class LessonRecord(models.Model):
    class Meta:
        db_table = 'lessonrecord'

    user_name = models.ForeignKey(User, verbose_name='顧客名', on_delete=models.CASCADE)
    lesson_name = models.ForeignKey(Lesson, verbose_name='ジャンル名', on_delete=models.CASCADE)
    lesson_date = models.DateField(default=timezone.now, verbose_name='受講日')
    lesson_hour = models.IntegerField(verbose_name='受講時間')

    def __str__(self):
        return self.user_name
