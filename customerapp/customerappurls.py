from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),

    path('categoryview/', views.categoryview, name="categoryview"),
    path('subcategoryview/<id>', views.subcategoryview, name="subcategoryview"),
    path('productview/<id>', views.productview, name="productview"),
    path('viewproductdetails/<id>', views.viewproductdetails, name='viewproductdetails'),
    path('cart_buy/<id>', views.cart_buy, name='cart_buy'),
    path('cartdetails/', views.cartdetails, name='cartdetails'),
    path('updateqty/', views.updateqty, name='updateqty'),
    path('payment/', views.payment, name='payment'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('removecartitem/<id>', views.removecartitem, name='removecartitem'),
    path('logout/', views.logout, name='logout'),
    path('customerprofile/', views.customerprofile, name='customerprofile'),
    path('edit/<id>', views.edit, name='edit'),
    path('selectlocation', views.selectlocation, name="selectlocation"),
    path('changepassword', views.changepassword, name="changepassword")
]
