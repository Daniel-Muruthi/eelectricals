from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('registeruser/',views.registeruser,name='registeruser'),
    path('login/', views.loginpage, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('home/', views.IndexView.as_view(), name='index')
]