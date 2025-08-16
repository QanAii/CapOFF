from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.UserRegisterView.as_view())
]
