from rest_framework import serializers
from .models import User,FriendshipRequest
class UserSerailzier(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','email','name','friends_count','get_avatar','posts_count')

class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)

    class Meta:
        model=FriendshipRequest
        fields=('id','created_by',)