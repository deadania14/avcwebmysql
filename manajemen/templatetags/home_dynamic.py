from django import template

from public.models import SettingsVariable

register = template.Library()

@register.simple_tag
def isi_desk():
    return SettingsVariable.objects.get(key='isi_deskripsi_home').value
