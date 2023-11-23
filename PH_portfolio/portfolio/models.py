from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to='portfolio/images')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

