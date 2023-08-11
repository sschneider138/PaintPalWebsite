from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='home', permanent=True)),
    path('home/', views.HomeView.as_view(), name='home'),
    path('usage/', views.UsageView.as_view(), name='usage'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('paintCalculator/', views.PaintCalculatorView.as_view(), name='paintCalculator'),
    path('login/', authViews.LoginView.as_view(template_name='Site/login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(template_name='Site/logout.html'), name='logout'),
    path('easterEgg/', views.EasterEgg.as_view(), name='easterEgg')

]
