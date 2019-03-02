from django import forms

from onlineschool.models import User
from onlineschool.models import LessonRecord

import datetime
from dateutil.relativedelta import relativedelta


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

    def clean_age(self):
        age = self.cleaned_data['age']
        if 0 > age or age > 120:
            raise forms.ValidationError("年齢は0-120歳の間で設定をお願い致します")
        return age


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

    def clean_lesson_hour(self):
        lesson_hour = self.cleaned_data['lesson_hour']
        if 0 > lesson_hour or lesson_hour > 12:
            raise forms.ValidationError("レッスン時間は1-12時間の間で設定をお願い致します")
        return lesson_hour


class InvoiceSearchForm(forms.Form):

    Month_CHOICES = (
        (datetime.date.today().month, datetime.date.today().strftime('%Y年%m月')),
        ((datetime.date.today()-relativedelta(months=1)).month, (datetime.date.today()-relativedelta(months=1)).strftime('%Y年%m月')),
        ((datetime.date.today()-relativedelta(months=2)).month, (datetime.date.today()-relativedelta(months=2)).strftime('%Y年%m月')),
    )

    invoice_search = forms.ChoiceField(
        label="請求書月別検索",
        choices=Month_CHOICES
    )

