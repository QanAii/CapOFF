from django.urls import path
from . import views
from .views import ProtectedView

urlpatterns = [
    path('user/register/', views.UserRegisterView.as_view()),
    path('user/protected/', ProtectedView.as_view()),
]
