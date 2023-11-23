# portfolio/views.py
from django.shortcuts import render, get_object_or_404
from .models import Photo


def photos(request):
    photos = Photo.objects.order_by("-id")
    return render(request, 'portfolio/portfolio.html', {'photos': photos})


def photo_details(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    return render(request, 'portfolio/photo-details.html', {'photo': photo})