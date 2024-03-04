from rest_framework import serializers
from account.serializers import UserSerailzier
from .models import Conversation,ConversationMessage

class ConversationSerializer(serializers.ModelSerializer):
    #model=Conversation
    users=UserSerailzier(read_only=True,many=True)
    class Meta:
        model=Conversation
        fields=('id','created_at','modified_at_formatted','users')


class ConversationMessageSerializer(serializers.ModelSerializer):
    created_by=UserSerailzier(read_only=True)
    sent_to=UserSerailzier(read_only=True)
    class Meta:
        model=ConversationMessage
        fields=('id','body','created_by','sent_to','created_at_formatted')

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages=ConversationMessageSerializer(read_only=True,many=True)
    class Meta:
        model=Conversation
        fields=('id','modified_at','messages','users')
    