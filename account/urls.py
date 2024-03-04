from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import api
urlpatterns=[
    path('me/',api.me,name="me"),
    path('editprofile/',api.editprofile,name='editprofile'),
    path('editpassword/',api.editpassword,name='editpassword'),
    path('signup/',api.signup,name="signup"),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain'),
    path('logout/',api.LogoutView.as_view(),name='logout'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('friends/<uuid:pk>/',api.friends,name='friends'),
    path('friends/request/<uuid:pk>/',api.friendRequest,name='friendRequest'),
    path('friends/<uuid:pk>/<str:status>/',api.handle_request,name='handle_request'),
    path('friends/suggested/', api.my_friendship_suggestions, name='my_friendship_suggestions'),
]