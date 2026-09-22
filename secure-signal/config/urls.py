from django.contrib.auth import views as auth
from django.urls import path
from scans import views

urlpatterns = [
    path("login/", auth.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path("scans/<int:pk>/", views.detail, name="detail"),
    path("scans/<int:pk>/delete/", views.delete, name="delete"),
]
