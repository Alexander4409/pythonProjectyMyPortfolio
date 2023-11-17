from django.forms import ModelForm
from .models import DTModel
from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Discount

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200,help_text="Required")
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class DTForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    your_name = forms.CharField(max_length=64)
    date_input = forms.DateField(widget=AdminDateWidget())
    time_input = forms.DateField(widget=AdminTimeWidget())
    end_time_input = forms.TimeField(widget=AdminTimeWidget())
    session_type_input = forms.ChoiceField(choices=DTModel.SESSION_TYPE_CHOICES)
    date_time_input = forms.DateField(widget=AdminSplitDateTime())


class DTModelForm(ModelForm):
    date_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    end_time = forms.TimeField(widget=AdminTimeWidget())
    session_type = forms.ChoiceField(choices=DTModel.SESSION_TYPE_CHOICES)
    price = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    duration = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    # favorites = forms.BooleanField(required=False)
    discount = forms.ModelChoiceField(queryset=Discount.objects.all(), required=False)

    class Meta:
        model = DTModel
        fields = ['name', 'date', 'time', 'end_time', 'session_type']
        widgets = {
            'date': AdminDateWidget(attrs={'required': False}),
            'time': AdminTimeWidget(attrs={'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_time'].widget = forms.HiddenInput()
        self.fields.pop('date_time', None)
        self.fields.pop('price', None)
        self.fields.pop('duration', None)
        self.fields.pop('discount', None)


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'start_date', 'end_date', 'amount']

