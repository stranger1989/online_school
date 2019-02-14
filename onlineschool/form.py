from django import forms

class aisatsuform(forms.Form):
    name = forms.CharField(label="name")
    area = forms.CharField(label="area")
    age = forms.IntegerField(label="age")