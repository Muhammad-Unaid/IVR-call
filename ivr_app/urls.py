from django.urls import path
from . import views

urlpatterns = [
    path('shopify/webhook/', views.shopify_webhook),
    path('ivr/', views.ivr),
    path('ivr/handle-input/', views.handle_input),
]
