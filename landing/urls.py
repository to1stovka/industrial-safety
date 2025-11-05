from django.urls import path
from landing.views import index, contact, nok_page, callback_request, minstroy_page

urlpatterns = [
    path("callback/", callback_request, name="callback_request"),
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path("nok/", nok_page, name="nok"),
    path("minstroy/", minstroy_page, name="minstroy"),
]