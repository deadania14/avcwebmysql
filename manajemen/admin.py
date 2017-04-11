from django.contrib import admin
from .models import Article, Practice, PracticeAttendance, Kelas, Administrasi, AdministrationType

admin.site.register(Article)
admin.site.register(Practice)
admin.site.register(PracticeAttendance)
admin.site.register(Kelas)
admin.site.register(Administrasi)
admin.site.register(AdministrationType)
