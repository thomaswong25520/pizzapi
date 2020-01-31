from django.urls import path

from . import views

urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("menu/mycart", views.cart, name="cart"),
    path('signup/', views.signup, name='signup'),
]
