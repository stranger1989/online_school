from django import template
from django.db.models import Sum, Count

from onlineschool.models import LessonRecord, Discount

register = template.Library()


@register.filter(name='mlti')
def mlti(value1, value2):
    total = value1 * value2
    return total


@register.filter(name='total_lesson_hour')
def total_lesson_hour(lesson_pay, lesson):
    # 現在の合計受講時間をユーザー・レッスン・月別に集計
    total_lesson_hour = LessonRecord.objects.all().filter(
        lesson_name=lesson.lesson_name,
        user_name=lesson.user_name,
        lesson_date__month=lesson.lesson_date.month,
        id__lte=lesson.id
    ).aggregate(Sum('lesson_hour'))

    # 前回までの合計受講時間をユーザー・レッスン・月別に集計
    previous_total_lesson_hour = LessonRecord.objects.all().filter(
        lesson_name=lesson.lesson_name,
        user_name=lesson.user_name,
        lesson_date__month=lesson.lesson_date.month,
        id__lt=lesson.id
    ).aggregate(Sum('lesson_hour'))

    discount_rate = Discount.objects.order_by('-limited_hour').filter(lesson_name_id=lesson.lesson_name.id)
    discount_rate_list = list(discount_rate)
    discount_level_count = 0

    # もし割引がない時、従量基本料金で計算
    if not discount_rate_list:
        return total_lesson_hour['lesson_hour__sum'] * lesson_pay

    # もし割引がある時、従量基本料金にいくら割引するか計算
    for discount_info in discount_rate:
        # 合計受講時間が閾値以上あるとき
        if total_lesson_hour['lesson_hour__sum'] >= discount_info.limited_hour:
            final_lesson_charge = 0
            deff_from_limited = total_lesson_hour['lesson_hour__sum'] - discount_rate_list[0].limited_hour

            if len(discount_rate) - 1 != discount_level_count:
                lesson_pay = discount_rate[discount_level_count + 1].discount_price

            # 受講時間が閾値をまたいでいない時
            if lesson.lesson_hour - deff_from_limited < 0:
                final_lesson_charge = lesson.lesson_hour * discount_rate_list[0].discount_price
            # 受講時間が閾値をまたいでいる時
            else:
                # 閾値を超えた分は割引額で計算
                final_lesson_charge += deff_from_limited * discount_rate_list[0].discount_price
                # 閾値以下分は割引前の額で計算
                final_lesson_charge += (lesson.lesson_hour - deff_from_limited) * lesson_pay
            return final_lesson_charge

        # 合計受講時間が閾値以下の時
        else:
            if len(discount_rate_list) == 1:
                # 合計受講時間が最小割引閾値を超えない時
                if total_lesson_hour['lesson_hour__sum'] <= lesson.lesson_name.free_time:
                    return 0
                elif previous_total_lesson_hour[
                        'lesson_hour__sum'] is not None:
                    if previous_total_lesson_hour[
                        'lesson_hour__sum'] < lesson.lesson_name.free_time and lesson.lesson_hour > lesson.lesson_name.free_time:
                        return (lesson.lesson_hour - (lesson.lesson_name.free_time - previous_total_lesson_hour['lesson_hour__sum'])) * lesson_pay
                elif total_lesson_hour['lesson_hour__sum'] > lesson.lesson_name.free_time and lesson.lesson_hour > lesson.lesson_name.free_time:
                    return (lesson.lesson_hour - lesson.lesson_name.free_time) * lesson_pay
                else:
                    return total_lesson_hour['lesson_hour__sum'] * lesson_pay
            else:
                # 閾値の最大値を削除
                discount_rate_list.pop(0)
                discount_level_count += 1


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

    month_lesson_genre = LessonRecord.objects.all().filter(
        user_name=user.id,
        lesson_date__month=month,
    )

    if month_lesson_charge['lesson_charge__sum'] is None:
        total_basic_charge = 0
    else:
        total_basic_charge = month_lesson_charge['lesson_charge__sum']
        if month_lesson_genre.exists():
            genre_list = []
            for lesson_genre in month_lesson_genre:
                if str(lesson_genre.lesson_name) not in genre_list:
                    total_basic_charge += lesson_genre.lesson_name.basic_charge
                genre_list.append(str(lesson_genre.lesson_name))

    return total_basic_charge

