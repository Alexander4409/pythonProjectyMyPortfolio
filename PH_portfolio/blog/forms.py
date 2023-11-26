from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

from .models import Blog


class BlogForm(forms.ModelForm):
    # date_input = forms.DateField(widget=AdminDateWidget())
    class Meta:
        model = Blog
        fields = ['title', 'description', 'date']
        widgets = {
            'date': AdminDateWidget(attrs={'required': False}),
            'time': AdminTimeWidget(attrs={'required': False}),
        }
