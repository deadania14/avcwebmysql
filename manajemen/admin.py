from django.contrib import admin
from .models import Article, Practice, PracticeAttendance, Kelas, Administrasi, AdministrationType, Inventory

class PracticeAttendanceInline(admin.TabularInline):
    model = PracticeAttendance
    fields = ('kelas', 'tutor', 'updated_date')
    max_num = 1

class PracticeAdmin(admin.ModelAdmin):
    model = Practice
    list_display = ['date', 'place', 'created_date',]
    inlines = (PracticeAttendanceInline,)
admin.site.register(Practice, PracticeAdmin)

class article(admin.ModelAdmin):
    model = Article
    list_display = ['title', 'author', 'is_mainarticle',]
admin.site.register(Article, article)

from ajax_select import make_ajax_form
class PracticeAttendanceAdmin(admin.ModelAdmin):
    form = make_ajax_form(PracticeAttendance, {
        # fieldname: channel_name
        'daftar_orang': 'users'
    })
    list_display = ['kelas','practice','tutor',]
admin.site.register(PracticeAttendance, PracticeAttendanceAdmin)

# @admin.register(Document)
# class DocumentAdmin(AjaxSelectAdmin):



class KelasAdmin(admin.ModelAdmin):
    list_display = ['nama_kelas', "updated_date",]
    search_fields = ['nama_kelas']
admin.site.register(Kelas, KelasAdmin)
admin.site.register(AdministrationType)

class inventories(admin.ModelAdmin):
    list_display = ['thingsname','stock','updated_date',]
admin.site.register(Inventory, inventories)

class administrasis(admin.ModelAdmin):
    list_display = ['user','jenis','method','status',]
admin.site.register(Administrasi, administrasis)
