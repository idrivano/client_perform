from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),

    path('clients/', clients, name='clients'),
    path('clients/<int:id>/report/', client_report, name='client_report'),
    path('clients/<int:id>/report/<int:pk>/task/', client_task, name='client_task'),
    path('clients/<int:id>/service/', client_service, name='client_service'),
    path('clients/<int:id>/support/', client_support, name='client_support'),

    path('products/', products, name='products'),
    path('products/<int:id>/', product_order, name='product_order'),

    path('services/', services, name='services'),
    path('supports/', supports, name='supports'),
    path('reports/', reports, name='reports'),
]