from django import template
from django.db.models import Sum, Count

from onlineschool.models import LessonRecord

register = template.Library()


@register.filter(name='mlti')
def mlti(value1, value2):
    total = value1 * value2
    return total


@register.filter(name='month_lesson_genre')
def month_lesson_genre(month, user):
    month_lesson_genre = LessonRecord.objects.all().filter(
        user_name=user.id,
        lesson_date__month=month,
    )

    genre_list = []
    for lesson_genre in month_lesson_genre:
        genre_list.append(lesson_genre.lesson_name.name)

    return '{0} ({1})'.format(' / '.join(list(set(genre_list))), str(len(list(set(genre_list)))))


@register.filter(name='month_lesson_count')
def month_lesson_count(month, user):
    month_lesson_count = LessonRecord.objects.all().filter(
        user_name=user.id,
        lesson_date__month=month,
    ).aggregate(Count('id'))
    return month_lesson_count['id__count']


@register.filter(name='month_lesson_charge')
def month_lesson_charge(month, user):
    month_lesson_charge = LessonRecord.objects.all().filter(
        user_name=user.id,
        lesson_date__month=month,
    ).aggregate(Sum('lesson_charge'))

    if month_lesson_charge['lesson_charge__sum'] is None:
        total_basic_charge = 0
    else:
        total_basic_charge = month_lesson_charge['lesson_charge__sum']

    return total_basic_charge


@register.filter(name='month_lesson_count_genre_sex')
def month_lesson_count_sex_genre(month, params):
    month_lesson_count_sex_genre = LessonRecord.objects.all().filter(
        lesson_name__name=params[0],
        user_name__sex=params[1],
        lesson_date__month=month,
    ).aggregate(Count('id'))
    return month_lesson_count_sex_genre['id__count']


@register.filter(name='month_user_count_genre_sex')
def month_user_count_genre_sex(month, params):
    month_user_count_genre_sex = LessonRecord.objects.all().filter(
        lesson_name__name=params[0],
        user_name__sex=params[1],
        lesson_date__month=month,
    ).values_list('user_name', flat=True).order_by('user_name').distinct().count()

    return month_user_count_genre_sex


@register.filter(name='month_lesson_charge_genre_sex')
def month_lesson_charge_genre_sex(month, params):
    month_lesson_charge_genre_sex = LessonRecord.objects.all().filter(
        lesson_name__name=params[0],
        user_name__sex=params[1],
        lesson_date__month=month,
    ).aggregate(Sum('lesson_charge'))

    if month_lesson_charge_genre_sex['lesson_charge__sum'] is None:
        month_lesson_charge_genre_sex = 0
    else:
        month_lesson_charge_genre_sex = month_lesson_charge_genre_sex['lesson_charge__sum']
    return month_lesson_charge_genre_sex


@register.filter(name='month_lesson_count_genre_sex_age')
def month_lesson_count_genre_sex_age(month, params):
    month_lesson_count_genre_sex_age = LessonRecord.objects.all().filter(
        lesson_name__name=params[0],
        user_name__sex=params[1],
        user_name__age__gte=int(params[2]),
        user_name__age__lte=int(params[2]) + 9,
        lesson_date__month=month,
    ).aggregate(Count('id'))
    return month_lesson_count_genre_sex_age['id__count']


@register.filter(name='month_user_count_genre_sex_age')
def month_user_count_genre_sex_age(month, params):
    month_user_count_genre_sex_age = LessonRecord.objects.all().filter(
        lesson_name__name=params[0],
        user_name__sex=params[1],
        user_name__age__gte=int(params[2]),
        user_name__age__lte=int(params[2]) + 9,
        lesson_date__month=month,
    ).values_list('user_name', flat=True).order_by('user_name').distinct().count()

    return month_user_count_genre_sex_age


@register.filter(name='month_lesson_charge_genre_sex_age')
def month_lesson_charge_genre_sex_age(month, params):
    month_lesson_charge_genre_sex_age = LessonRecord.objects.all().filter(
        lesson_name__name=params[0],
        user_name__sex=params[1],
        user_name__age__gte=int(params[2]),
        user_name__age__lte=int(params[2]) + 9,
        lesson_date__month=month,
    ).aggregate(Sum('lesson_charge'))

    if month_lesson_charge_genre_sex_age['lesson_charge__sum'] is None:
        month_lesson_charge_genre_sex_age = 0
    else:
        month_lesson_charge_genre_sex_age = month_lesson_charge_genre_sex_age['lesson_charge__sum']
    return month_lesson_charge_genre_sex_age
