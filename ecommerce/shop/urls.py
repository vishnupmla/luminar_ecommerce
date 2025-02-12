"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    path('',views.homeView,name = 'home'),
    path('products <int:pk>',views.ProductDetail.as_view(),name= 'products'),
    path('productdetail<int:pk>',views.SingleProductDetail.as_view(),name='productdetails'),
    path('register',views.userRegister,name='register'),
    path('login',views.userLogin,name='login'),
    path('logout', views.userLogout,name='logout'),
    path('trackorders',views.trackOrders,name='trackorders'),
    path('about', views.aboutUs, name='about'),
    path('addcategory',views.AddCategory.as_view(),name='addcategory'),
    path('addproducts',views.AddProduct.as_view(),name='addproducts'),
    path('addstock/<int:pk>/',views.AddStock.as_view(),name='addstock'),
]
