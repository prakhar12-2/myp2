from . import api
from django.urls import path
urlpatterns=[
    path('',view=api.PostView, name='Posts'),
    path('create/',view=api.post_create,name='post_create'),
    path('profile/<uuid:id>/',view=api.post_list_profile,name='post_list_profile'),
    path('like/<uuid:pk>/',view=api.post_like,name='post_like'),
    path('comment/<uuid:pk>/',view=api.comment_create,name='comment_create'),
    path('<uuid:pk>/',view=api.post_detail,name='post_detail'),
    path('trends/',view=api.trends_detail,name='trends_detail')
]