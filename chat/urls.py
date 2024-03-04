from django.urls import path
from . import api
urlpatterns=[
    path('',api.conversation_list,name='conversation_list'),
    path('<uuid:pk>/',api.conversation_detail,name='conversation_detail'),
    path('<uuid:pk>/send/',api.send_message,name='send_message'),
    path('<uuid:pk>/get_or_start/',api.get_or_start,name='get_or_start')
]