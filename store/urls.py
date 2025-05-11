from django.urls import path
from . import views

urlpatterns = [
    path('',views.intro,name="intro"),
    path('store/',views.store,name='store'),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('intro/',views.intro,name='intro'),
    path('about/',views.about,name='about'),
]
