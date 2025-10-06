from django.urls import path
from landing.views import index, contact

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
]