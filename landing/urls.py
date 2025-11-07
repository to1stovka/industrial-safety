from django.urls import path
from landing.views import (
    index,
    contact, 
    nok_page, 
    callback_request, 
    minstroy_page, 
    minstroy_list,
    exam,
    qualifications_list,
    attestation
    )

urlpatterns = [
    path("callback/", callback_request, name="callback_request"),
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path("nok/", nok_page, name="nok"),
    path("minstroy/", minstroy_page, name="minstroy"),
    path('minstroy/list/', minstroy_list, name='list'),
    path('exam/', exam, name='exam'),
    path("qualifications/", qualifications_list, name="qualifications"),
    path("attestation/", attestation, name="attestation"),
]