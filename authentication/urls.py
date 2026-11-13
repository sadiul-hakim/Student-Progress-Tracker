from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import BootstrapAuthenticationForm

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="authentication/login.html",
            authentication_form=BootstrapAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
