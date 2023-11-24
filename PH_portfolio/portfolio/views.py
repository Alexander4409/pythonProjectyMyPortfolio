from django.shortcuts import render, get_object_or_404
from .models import Photo

def slider_view(request):
    photos = Photo.objects.all()
    return render(request, 'portfolio/slider.html', {'photos': photos})

def image_detail_view(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    return render(request, 'portfolio/image_detail.html', {'photo': photo})
