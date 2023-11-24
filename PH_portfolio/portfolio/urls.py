from django.urls import path
from .views import slider_view, image_detail_view

app_name = 'portfolio'

urlpatterns = [
    path('slider/', slider_view, name='slider'),
    path('image/<int:photo_id>/', image_detail_view, name='image_detail'),
]
