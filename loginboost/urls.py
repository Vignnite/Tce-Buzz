from django.contrib import admin
from django.urls import path,include
from loginboost import views
urlpatterns = [
    path('',views.lobby,name = 'lobby'),
    path('signup',views.signup,name = 'signup'),
    path('signin',views.signin,name = 'signin'), 
    path('signout',views.signout,name = 'signout'),
    path('activate/<uidb64>/<token>',views.activate,name = 'activate'),
    path('avc',views.avc,name = 'avc'),
    path('Meet',views.Meet,name = 'Meet')
]