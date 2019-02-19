from django.contrib import admin
from .models import User, Lesson, LessonRecord

admin.site.register(User)
admin.site.register(Lesson)
admin.site.register(LessonRecord)
