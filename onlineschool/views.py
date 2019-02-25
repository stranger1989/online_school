from django.db.models import Sum
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User, LessonRecord, Discount
from .form import UserForm, LessonRecordForm, InvoiceSearchForm
import datetime


def index(request):
    params = {
        'title': 'メニュー',
    }
    return render(request, 'onlineschool/index.html', params)


# ユーザー関連
def user_list(request):
    params = {
        'title': '顧客一覧',
        'users': User.objects.all(),
    }
    return render(request, 'onlineschool/user_list.html', params)


def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('onlineschool:user_list'))
        else:
            params = {
                'title': '顧客登録',
                'form': form
            }
            return render(request, 'onlineschool/user_new.html', params)
    else:
        params = {
            'title': '顧客登録',
            'form': UserForm()
        }
    return render(request, 'onlineschool/user_new.html', params)


def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            return HttpResponseRedirect(reverse('onlineschool:user_list'))
    else:
        form = UserForm({'name': user.name, 'sex': user.sex, 'age': user.age})
        params = {
            'title': '顧客編集',
            'form': form,
            'user_id': user_id,
        }
    return render(request, 'onlineschool/user_edit.html', params)


def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    params = {
        'title': '顧客一覧',
        'users': User.objects.all(),
    }
    return render(request, 'onlineschool/user_list.html', params)


def lesson_list(request):
    params = {
        'title': 'レッスン一覧',
        'lessonrecords': LessonRecord.objects.all(),
    }
    return render(request, 'onlineschool/lesson_list.html', params)


def lesson_form(request):
    if request.method == 'POST':
        form = LessonRecordForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            lesson_with_charge = LessonRecord.objects.get(pk=lesson.id)
            if total_lesson_hour(lesson_with_charge.lesson_name.pay_per_charge, lesson_with_charge) is None:
                lesson_with_charge.lesson_charge = 0
            else:
                lesson_with_charge.lesson_charge = total_lesson_hour(lesson_with_charge.lesson_name.pay_per_charge, lesson_with_charge)
            lesson_with_charge.save()
            return HttpResponseRedirect(reverse('onlineschool:lesson_list'))
        else:
            return render(request, 'onlineschool/lesson_new.html', {'form': form})
    else:
        params = {
            'title': 'レッスン登録',
            'form': LessonRecordForm()
        }
    return render(request, 'onlineschool/lesson_new.html', params)


def lesson_edit(request, lesson_id):
    lesson = get_object_or_404(LessonRecord, pk=lesson_id)
    if request.method == 'POST':
        form = LessonRecordForm(request.POST, instance=lesson)
        if form.is_valid():
            lesson.save()
            lesson_with_charge = LessonRecord.objects.get(pk=lesson.id)
            lesson_with_charge.lesson_charge = total_lesson_hour(lesson_with_charge.lesson_name.pay_per_charge, lesson_with_charge)
            lesson_with_charge.save()
            return HttpResponseRedirect(reverse('onlineschool:lesson_list'))
    else:
        form = LessonRecordForm({
            'user_name': lesson.user_name.id,
            'lesson_name': lesson.lesson_name.id,
            'lesson_date': lesson.lesson_date,
            'lesson_hour': lesson.lesson_hour,
        })
        params = {
            'title': 'レッスン編集',
            'form': form,
            'lesson_id': lesson_id,
        }
    return render(request, 'onlineschool/lesson_edit.html', params)


def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(LessonRecord, pk=lesson_id)
    lesson.delete()
    params = {
        'title': 'レッスン一覧',
        'lessonrecords': LessonRecord.objects.all(),
    }
    return render(request, 'onlineschool/lesson_list.html', params)


def lesson_invoice(request):
    if request.method == 'POST':
        params = {
            'title': request.POST['invoice_search'] + '月レッスン請求一覧',
            'users': User.objects.all(),
            'form': InvoiceSearchForm(),
            'lesson_search_month': request.POST['invoice_search']
        }
        return render(request, 'onlineschool/lesson_invoice.html', params)
    else:
        params = {
            'title': 'レッスン請求一覧',
            'users': User.objects.all(),
            'form': InvoiceSearchForm(),
            'lesson_search_month': datetime.date.today().month
        }
        return render(request, 'onlineschool/lesson_invoice.html', params)


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
            # 合計受講時間が最小割引閾値を超えない時
            if len(discount_rate_list) == 1:
                # 合計受講時間が無料時間より少ないとき
                if total_lesson_hour['lesson_hour__sum'] <= lesson.lesson_name.free_time:
                    return 0
                else:
                    if previous_total_lesson_hour['lesson_hour__sum'] is not None:
                        if previous_total_lesson_hour['lesson_hour__sum'] < lesson.lesson_name.free_time and total_lesson_hour['lesson_hour__sum'] > lesson.lesson_name.free_time:
                            return (lesson.lesson_hour - (lesson.lesson_name.free_time - previous_total_lesson_hour['lesson_hour__sum'])) * lesson_pay
                        else:
                            return lesson.lesson_hour * lesson_pay
                    else:
                        return (lesson.lesson_hour - lesson.lesson_name.free_time) * lesson_pay
            else:
                # 閾値の最大値を削除
                discount_rate_list.pop(0)
                discount_level_count += 1
