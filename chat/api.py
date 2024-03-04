from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .models import Conversation,ConversationMessage
from .serializers import ConversationDetailSerializer,ConversationMessageSerializer,ConversationSerializer
from django.http import JsonResponse
from account.models import User

@api_view(['GET'])
def conversation_list(request):
    #print(request.user)
    conversations=Conversation.objects.filter(users__in=list([request.user]))
    serializer=ConversationSerializer(conversations,many=True)
    #print(conversations)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
def conversation_detail(request,pk):
    conversation=Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer=ConversationDetailSerializer(conversation)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def send_message(request,pk):
    conversation=Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    for user in conversation.users.all():
        if user.id!=request.user.id:
            sent_to=user
    message=ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        sent_to=sent_to,
        created_by=request.user
    )

    serializer=ConversationMessageSerializer(message)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
def get_or_start(request,pk):
    user=User.objects.get(pk=pk)
    conversations=Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))
    if conversations.exists():
        conversation=conversations.first()
    else:
        conversation=Conversation.objects.create()
        conversation.users.add(user,request.user)
        conversation.save()
    serializer=ConversationDetailSerializer(conversation)
    return JsonResponse(serializer.data,safe=False)

