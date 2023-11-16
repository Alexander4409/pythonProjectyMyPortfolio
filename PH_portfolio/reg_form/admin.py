from django.contrib import admin
from .models import DTModel
from .models import Discount
from .forms import DiscountForm
# Register your models here.

class DTMAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time',)


admin.site.register(DTModel, DTMAdmin)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm