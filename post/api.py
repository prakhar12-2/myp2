from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from .models import Post,Like,Comment,Trends
from .serializers import PostSerailzier,PostDetailSerializer,CommentSerailizer,TrendSerializer
from .forms import PostForm,PostAttachmentForm
from account.models import User,FriendshipRequest
from account.serializers import UserSerailzier
from notification.utils import create_notification
from django.db.models import Q
@api_view(['GET'])
def PostView(request):
    #posts=Post.objects.all()
    post_ids=[request.user.id]
    for friend in request.user.friends.all():
        post_ids.append(friend.id)
    posts=Post.objects.filter(created_by_id__in=list(post_ids))
    trend=request.GET.get('trend','')
    if trend:
        posts=posts.filter(body__icontains='#'+trend)
    serializers=PostSerailzier(posts,many=True)
    return JsonResponse(serializers.data,safe=False)

@api_view(['GET'])
def post_list_profile(request,id):
    posts=Post.objects.filter(created_by_id=id)
    user=User.objects.get(pk=id)
    can_send_friend_request=True
    if request.user in user.friends.all():
        can_send_friend_request = False
    check1=FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)
    check2=FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    if check1 or check2:
        can_send_friend_request=False
    pserializers=PostSerailzier(posts,many=True)
    userializers=UserSerailzier(user)
    return JsonResponse({'posts':pserializers.data,
                         'user':userializers.data,
                         'can_send_friend_request':can_send_friend_request
                         },safe=False)

@api_view(['POST'])
def post_create(request):
    form=PostForm(request.POST)
    attachment=None
    attachmentform=PostAttachmentForm(request.POST,request.FILES)
    if attachmentform.is_valid():
        attachment=attachmentform.save(commit=False)
        attachment.created_by=request.user
        attachment.save()

    if form.is_valid():
        post=form.save(commit=False)
        post.created_by=request.user
        post.save()
        if attachment:
            post.attachments.add(attachment)
            post.save()
        user=request.user
        user.posts_count=user.posts_count + 1
        user.save()
        serializers=PostSerailzier(post)
        return JsonResponse(serializers.data,safe=True)
    else:
       return JsonResponse({'error':'enter something else'})

@api_view(['POST'])
def post_like(request,pk):
    post=Post.objects.get(pk=pk)
    #post.like_count=1
    #post.save()
    #print(post.like_count)
    #print(post.like.filter(created_by=request.user))
   
    if not post.like.filter(created_by=request.user):
        like=Like.objects.create(created_by=request.user)
        post=Post.objects.get(pk=pk)
        post.like_count=post.like_count+1
        post.like.add(like)
        post.save()
        notification = create_notification(request, 'post_like', post_id=post.id)
        return JsonResponse({'message':'Liked the post'})
    else:
        return JsonResponse({'message':'Liked already'})

@api_view(['GET'])
def post_detail(request,pk):
    
    post=Post.objects.get(pk=pk)
    return JsonResponse({
        'post':PostDetailSerializer(post).data
    })

@api_view(['POST'])
def comment_create(request,pk):
    post=Post.objects.get(pk=pk)
    comment=Comment.objects.create(body=request.data.get('body'),created_by=request.user)
    post.comment.add(comment)
    post.comment_count=post.comment_count+1
    post.save()
    comment.save()
    notification = create_notification(request, 'post_comment', post_id=post.id)
    serializer=CommentSerailizer(comment)
    return JsonResponse(serializer.data,safe=True)    
    #print(request.data)
    #print(post.id)
    #return JsonResponse({'message':'new comment added'})

@api_view(['GET'])
def trends_detail(request):
    serializer=TrendSerializer(Trends.objects.all(),many=True)
    return JsonResponse(serializer.data,safe=False)