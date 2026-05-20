from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('register/', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
