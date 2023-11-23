from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.photos, name='photos'),
    path('<int:photo_id>/', views.photo_details, name='photo_details'),
]
