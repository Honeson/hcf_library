from django.urls import path
from .views import (
     admin_view, 
     publisher_view, 
     UserPostListView, 
     login_view, 
     logout_view, 
     user_registration_form,
     register_view,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
     # path('', login_form, name='home'),
     path('registerform/', user_registration_form, name='registerform'),
     path('register/', register_view, name='register'),
     path('login/', login_view, name='login'),
     path('logout/', logout_view, name='logout'),



     # System admin's URLs
     path('systemadmin/', admin_view, name='admin_dashboard'),

     # Publisher's URLs
     path('publisher/', publisher_view, name='publisher_dashboard'),


     # User's URLs
     path('user/', UserPostListView.as_view(), name='user_dashboard'),
]
