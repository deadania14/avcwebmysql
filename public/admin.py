from django.contrib import admin
from .models import Event, UserProfile, SettingsVariable, Slider, Timeline, QuestionAnswer

class userprofile(admin.ModelAdmin):
    list_display = ['user', 'phone', 'tipe_user','user_kelas',]
admin.site.register(UserProfile, userprofile)

class setvar(admin.ModelAdmin):
    list_display = ['key', 'value', 'updated_date',]
admin.site.register(SettingsVariable, setvar)

class slide(admin.ModelAdmin):
    list_display = ['caption', 'publisher', 'updated_date',]
admin.site.register(Slider, slide)

class event(admin.ModelAdmin):
    list_display = ['event_name', 'sender', 'phone', 'event_date','event_status',]
admin.site.register(Event, event)

class timeline(admin.ModelAdmin):
    list_display = ['title', 'message', 'created_date', 'writer']
admin.site.register(Timeline, timeline)

class questionanswer(admin.ModelAdmin):
    list_display = ['question', 'answer', 'created_date', 'updated_date']
admin.site.register(QuestionAnswer, questionanswer)
