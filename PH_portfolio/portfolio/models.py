from django.db import models

class Image(models.Model):
    photo = models.ForeignKey('Photo', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/images')

    def __str__(self):
        return str(self.image)

class Photo(models.Model):
    CATEGORY_CHOICES = [
        ('wedding', 'Свадебные'),
        ('animal', 'Анималистические'),
        ('love_story', 'Лавстори'),
        ('studio', 'Студийные'),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
