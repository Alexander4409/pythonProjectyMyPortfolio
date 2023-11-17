from django.urls import path
from .import views


app_name = 'reg_form'

urlpatterns = [
    #authorisation
    path('signup/', views.signupuser, name='signup'),
    path('logout/', views.logoutuser, name='logout'),
    path('login/', views.loginuser, name='login'),

    #RegForm
    path('currentRegForm_v2/', views.currentRegForm_v2, name="currentRegForm_v2"),
    path('photosessions/', views.photosessions, name='photosessions'),
    path('edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path('delete/<int:record_id>/', views.delete_record, name='delete_record'),
    path('upcoming_photosessions/', views.upcoming_photosessions, name='upcoming_photosessions'),

    path('discounts/', views.manage_discounts, name='manage_discounts'),
    path('discounts/edit/<int:discount_id>/', views.edit_discount, name='edit_discount'),
    path('discounts/delete/<int:discount_id>/', views.delete_discount, name='delete_discount'),
    path('discounts/create/', views.create_discount, name='create_discount'),
]