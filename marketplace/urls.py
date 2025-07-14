from django.urls import path, include
from .views import *


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path("my_store/", MyStoreView.as_view(), name="mystore"),
    path("start_selling/", StartSellingView.as_view(), name="start_selling"),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    ]
