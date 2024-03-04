from rest_framework import serializers
from .models import Post,Comment,Trends,PostAttachments
from account.serializers import UserSerailzier
class PostAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostAttachments
        fields=('id','get_image')


class PostSerailzier(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)
    attachments=PostAttachmentsSerializer(read_only=True,many=True)
    class Meta:
        model=Post
        fields=('id','body','is_private','created_at_formatted','created_by','like_count','comment_count','attachments',)
    
class CommentSerailizer(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)
    class Meta:
        model=Comment
        fields=('id','body','created_at_formatted','created_by')

class PostDetailSerializer(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)
    comment=CommentSerailizer(read_only=True,many=True)
    attachments=PostAttachmentsSerializer(read_only=True,many=True)
    class Meta:
        model=Post
        fields=('id','body','created_at_formatted','created_by','like_count','comment','comment_count','attachments')
    
class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trends
        fields=('id','hashtag','occurances')