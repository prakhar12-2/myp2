from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from account.models import User
from account.serializers import UserSerailzier
from post.models import Post
from post.serializers import PostSerailzier
@api_view(['POST'])
def search(request):
    data=request.data
    query=data['query']
    user=User.objects.filter(name__icontains=query)
    uSerailzier=UserSerailzier(user,many=True)
    post=Post.objects.filter(body__icontains=query)
    pSerailzier=PostSerailzier(post,many=True)
    return JsonResponse({
        'users':uSerailzier.data,
        'posts':pSerailzier.data
    },safe=False)