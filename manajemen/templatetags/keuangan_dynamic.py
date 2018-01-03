from django import template

from public.models import SettingsVariable

register = template.Library()

@register.simple_tag
def saldo():
    return SettingsVariable.objects.get(key='saldo').value

@register.simple_tag
def nomor_rekening():
    return SettingsVariable.objects.get(key='nomer_rekening_keuangan').value
