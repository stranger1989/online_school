from django import forms

from onlineschool.models import User
from onlineschool.models import LessonRecord


class UserForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=User.SEX_CHOICES, label='性別')

    class Meta:
        model = User
        fields = ('name', 'sex', 'age',)
        labels = {
            'name': '名前',
            'sex': '性別',
            'age': '年齢'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LessonRecordForm(forms.ModelForm):

    class Meta:
        model = LessonRecord
        fields = ('user_name', 'lesson_name', 'lesson_date', 'lesson_hour')
        labels = {
            'user_name': '顧客名',
            'lesson_name': 'ジャンル',
            'lesson_date': '受講日',
            'lesson_hour': '受講時間(h)',
        }
