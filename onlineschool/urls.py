from django.urls import path
from . import views

app_name = 'onlineschool'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_list', views.user_list, name='user_list'),
    path('user_form', views.user_form, name='user_form'),
    path('user_form/<int:user_id>/', views.user_edit, name='user_edit'),
    path('user_delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('lesson_list', views.lesson_list, name='lesson_list'),
    path('lesson_form', views.lesson_form, name='lesson_form'),
    path('lesson_form/<int:lesson_id>/', views.lesson_edit, name='lesson_edit'),
    path('lesson_delete/<int:lesson_id>/', views.lesson_delete, name='lesson_delete'),
]
