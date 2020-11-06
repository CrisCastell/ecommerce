from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart', views.cart, name="cart"),
    path('checkout', views.checkout, name="checkout"),
    path('category/<str:name>', views.category, name="category"),
    path('profile', views.profile, name="profile"),
    path('product/<int:id>', views.detailView, name="detail-view"),
    path('admin-control', views.adminControl, name="admin-control"),




    #api
    path("update-order", views.updateOrder, name="update-order"),
    path("order-info", views.orderInfo, name="order-info"),
    path("process-order", views.processOrder, name="process-order"),
    path("shippings-api", views.shippings, name="shippings-api"),


    #User signup and authentication
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]