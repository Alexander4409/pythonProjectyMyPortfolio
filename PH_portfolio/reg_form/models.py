# from django.db import models
# from django.contrib.auth.models import User
# # Create your models here.
#
#
# class DTModel(models.Model):
#     SESSION_TYPE_CHOICES = (
#         ('standard', 'Стандартная'),
#         ('advanced', 'Продвинутая'),
#         ('premium', 'Премиум'),
#     )
#     name = models.CharField(max_length=64,null=True)
#     date = models.DateField(null=True)
#     time = models.TimeField(null=True)
#     end_time = models.TimeField(null=True)
#     session_type = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES, default='standard')
#     date_time = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return self.name

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class DTModel(models.Model):
    SESSION_TYPE_CHOICES = (
        ('standard', 'Стандартная'),
        ('advanced', 'Продвинутая'),
        ('premium', 'Премиум'),
    )
    name = models.CharField(max_length=64, null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    session_type = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES, default='standard')
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_duration_and_price(self):
        start_datetime = datetime.combine(self.date, self.time)
        end_datetime = datetime.combine(self.date, self.end_time)
        duration = (end_datetime - start_datetime).seconds / 3600  # Продолжительность в часах
        if self.session_type == 'standard':
            price = duration * 100
        elif self.session_type == 'advanced':
            price = duration * 200
        elif self.session_type == 'premium':
            price = duration * 300
        else:
            price = 0  # Обработка других типов
        self.duration = round(duration, 2)
        self.price = round(price, 2)
