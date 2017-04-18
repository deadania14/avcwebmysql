from django.contrib import admin
from .models import Article, Practice, PracticeAttendance, Kelas, Administrasi, AdministrationType


class PracticeAttendanceInline(admin.TabularInline):
    model = PracticeAttendance
    fields = ('kelas', 'tutor', 'updated_date')
    max_num = 1

class PracticeAdmin(admin.ModelAdmin):
    model = Practice
    list_display = ['date', 'place', 'created_date',]
    inlines = (PracticeAttendanceInline,)
admin.site.register(Practice, PracticeAdmin)

admin.site.register(Article)

class PracticeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['kelas','practice','tutor',]
admin.site.register(PracticeAttendance, PracticeAttendanceAdmin)

class KelasAdmin(admin.ModelAdmin):
    list_display = ['nama_kelas', "updated_date",]
    search_fields = ['nama_kelas']
admin.site.register(Kelas, KelasAdmin)
admin.site.register(Administrasi)
admin.site.register(AdministrationType)
