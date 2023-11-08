from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal
from django.utils import timezone


class Discount(models.Model):
    name = models.CharField(max_length=64)  # Название скидки
    start_date = models.DateTimeField()  # Дата и время начала скидки
    end_date = models.DateTimeField()  # Дата и время окончания скидки
    amount = models.DecimalField(max_digits=5, decimal_places=2)  # Размер скидки в процентах

    def __str__(self):
        return self.name


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
    favorites = models.ManyToManyField(User, related_name='favorite_photosessions', blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    def calculate_duration_and_price(self):
        start_datetime = datetime.combine(self.date, self.time)
        end_datetime = datetime.combine(self.date, self.end_time)
        duration = Decimal((end_datetime - start_datetime).seconds) / Decimal(3600)  # Продолжительность в часах
        if self.session_type == 'standard':
            base_price = duration * Decimal(100)
        elif self.session_type == 'advanced':
            base_price = duration * Decimal(200)
        elif self.session_type == 'premium':
            base_price = duration * Decimal(300)
        else:
            base_price = Decimal(0)  # Обработка других типов

        # Проверяем, есть ли применяемая скидка
        # if self.discount and self.discount.start_date <= datetime.now() <= self.discount.end_date:
        if self.discount and self.discount.start_date <= timezone.now() <= self.discount.end_date:
            discount_amount = self.discount.amount
        else:
            discount_amount = Decimal(0)

        # Учитываем скидку
        discounted_price = base_price - (base_price * (discount_amount / Decimal(100)))

        self.duration = round(duration, 2)
        self.price = round(discounted_price, 2)

    def save(self, *args, **kwargs):
        self.calculate_duration_and_price()
        super().save(*args, **kwargs)