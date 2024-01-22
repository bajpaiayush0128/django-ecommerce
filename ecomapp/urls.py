from django.urls import path
from ecomapp import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('blog/', views.blog, name="blog"),
    path('orders/', views.orders, name="orders"),
    path('profile/', views.profile, name="profile"),
    path('checkout/', views.checkout, name="checkout"),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
    path('webhook/stripe', views.my_webhook_view, name='my_webhook_view'),
]
