from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class DTModel(models.Model):
    name = models.CharField(max_length=64,null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    date_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name