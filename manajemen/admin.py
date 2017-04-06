from django.contrib import admin
from .models import Article, Practice, PracticeAttendance

admin.site.register(Article)
admin.site.register(Practice)
admin.site.register(PracticeAttendance)
