from django import forms
from waterpark.models import Tiket, SeasonPass
from datetime import date


class TiketForm(forms.ModelForm):
    class Meta:
        model = Tiket
        fields = ['validity_day']
        fields_required = ['validity_day']
        widgets = {
            'validity_day': forms.SelectDateWidget(empty_label=('Year', 'Month', 'Day'), years=range(date.today().year, date.today().year+2)),
        }


class SeasonPassForm(forms.ModelForm):
    class Meta:
        model = SeasonPass
        fields = ['seasonpass_photo']
        fields_required = ['seasonpass_photo']
