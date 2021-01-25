from django import forms
from .models import Asset, Schedule
from django.utils.translation import gettext_lazy as _

class AssetForm(forms.ModelForm):

    class Meta:
        model  = Asset
        fields = ['asset_name', 'user_email', 'up_price', 'low_price']

        labels  = {
            'asset_name': _('ativo'),
            'user_email': _('email do usuário'),
            'up_price': _('preço de venda'),
            'low_price': _('preço de compra'),
        }

class ScheduleForm(forms.ModelForm):

    class Meta:
        model  = Schedule
        fields = ['minutes']

        labels  = { 'minutes': _('tempo de consulta') }