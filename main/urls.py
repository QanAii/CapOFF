from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('catalog/', views.CatalogView.as_view()),
    path('index/products/<int:product_id>/', views.ProductDetailView.as_view()),
    path('products/<int:pk>/like/', views.LikeView.as_view()),
]
