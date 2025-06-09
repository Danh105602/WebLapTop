from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/form/', views.checkout_form_view, name='checkout_form'),
    path('profile/', views.profile_view, name='profile'),
    path('order-history/', views.order_history_view, name='order_history'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('update-order-address/<int:order_id>/', views.update_order_address, name='update_order_address'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('add-product/', views.add_product, name='add_product'),
    path('search/', views.product_search, name='product_search'),
    path('news/', views.news_list, name='news_list'), # tin tức
    path('policy/', views.policy_view, name='policy'),# chinh sach
    path('contact/', views.contact_view, name='contact'),#Lien he
    #path('order/<int:order_id>/update_address/', views.update_order_address, name='update_order_address'), # CN địa chỉ 
    #path('evaluate/<int:order_id>/', views.evaluate, name='evaluate'),
]
