from django.contrib import admin
from .models import Event, UserProfile, SettingsVariable

admin.site.register(Event)
admin.site.register(UserProfile)

class setvar(admin.ModelAdmin):
    list_display = ['key', 'value', 'updated_date',]
admin.site.register(SettingsVariable, setvar)
