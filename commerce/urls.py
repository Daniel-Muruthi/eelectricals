from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('registeruser/',views.registeruser,name='registeruser'),
    path('login/', views.loginpage, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('home/', views.index, name='index'),
	path('description/<int:pk>/', views.DescriptionView.as_view(), name='description'),
	path('addproduct/', views.descriptionView, name="addproduct"),
	path('productlist/', views.product_list, name="productlist"),
	path('products/', views.myproducts, name="myproducts")
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)