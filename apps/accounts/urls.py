# accounts/urls.py

from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/',views.Login,name='Login'),
    path("logout/",views.Logout,name="Logout"),
    path('guest_login/', views.guest_login, name = 'guest_login'), #かんたんログイン用
]