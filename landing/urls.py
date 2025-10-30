from django.urls import path
from landing.views import index, contact, nok_page

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path("nok/", nok_page, name="nok"),
]