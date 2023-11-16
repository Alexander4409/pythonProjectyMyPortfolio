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





]