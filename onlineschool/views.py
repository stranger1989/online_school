from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User, LessonRecord
from .form import UserForm, LessonRecordForm


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
            form.save()
            return HttpResponseRedirect(reverse('onlineschool:lesson_list'))
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
            return HttpResponseRedirect(reverse('onlineschool:lesson_list'))
    else:
        form = LessonRecordForm({
            'user_name': lesson.user_name,
            'lesson_name': lesson.lesson_name,
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
