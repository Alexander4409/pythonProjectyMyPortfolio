from django.forms import ModelForm
from .models import DTModel
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.auth.models import User


class DTForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    your_name = forms.CharField(max_length=64)
    date_input = forms.DateField(widget=AdminDateWidget())
    time_input = forms.DateField(widget=AdminTimeWidget())
    date_time_input = forms.DateField(widget=AdminSplitDateTime())


class DTModelForm(ModelForm):
    date_time = forms.SplitDateTimeField(widget=AdminSplitDateTime(attrs={'style': 'display:none;'}))
    class Meta:
        model = DTModel
        fields = ['name', 'date', 'time']
        widgets = {
            'date': AdminDateWidget(),
            'time': AdminTimeWidget(),
        }

