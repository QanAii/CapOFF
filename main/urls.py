from django.urls import path
from . import views
from .views import LikeView


urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('catalog/', views.CatalogView.as_view()),
    path('index/products/<int:product_id>/', views.ProductDetailView.as_view()),
    path('basket/add/', views.BasketAddView.as_view()),

    path('like/<int:product_id>/', LikeView.as_view(), name='like-toggle'),
    path('likes/', LikeView.as_view(), name='like-list'),
]
