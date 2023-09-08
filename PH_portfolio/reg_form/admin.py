from django.contrib import admin
from .models import DTModel
# Register your models here.


class DTMAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time',)


admin.site.register(DTModel, DTMAdmin)
