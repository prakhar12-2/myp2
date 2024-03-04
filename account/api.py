from rest_framework.decorators import api_view,authentication_classes,permission_classes
from django.http import JsonResponse
from .forms import SignupForm,ProfileForm
from .models import User,FriendshipRequest
from .serializers import UserSerailzier,FriendshipRequestSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from notification.utils import create_notification
from django.conf import settings

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET"])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name':request.user.name,
        'email':request.user.email,
        'avatar':request.user.get_avatar()
    })

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })
    if form.is_valid():
        user = form.save()
        user.is_active = True
        #user.save()
        #url=f"{settings.WEBSITE_URL}/activateaccount/?email={user.email}&id={user.id}"
        #send_mail(
         #"Verification mail",
         #f"Click on the link to verify : {url}",
         #"noreply-myp@mail.com",
         #[user.email],
        #fail_silently=False,
       #)
    else:
        message = form.errors.as_json()
        #message='error'
    
    print(message)

    return JsonResponse({'message': message}, safe=False)

@api_view(['POST'])
def friendRequest(request,pk):
    user=User.objects.get(pk=pk)
    check1=FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)
    check2=FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    if not check1 or not check2:
        friendRequestmod=FriendshipRequest.objects.create(created_by=request.user,created_for=user,status='Sent')
        notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendRequestmod.id)
        return JsonResponse({'message':'Request Sent successfully'})
    else:
       return JsonResponse({'message':'Request has been sent already'})
       
    
@api_view(['GET'])
def friends(request,pk):
    user=User.objects.get(pk=pk)
    requests=[]

    if user==request.user:
        requests=FriendshipRequest.objects.filter(created_for=request.user,status=FriendshipRequest.SENT)
        requests=FriendshipRequestSerializer(requests,many=True)
        requests=requests.data

    friends=user.friends.all()
    return JsonResponse({
        'user':UserSerailzier(user).data,
        'friends':UserSerailzier(friends, many=True).data,
        'requests':requests,
    },safe=True)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def handle_request(request,pk,status):
    user=User.objects.get(pk=pk)#who sent the request
    friend_Request=FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friend_Request.status=status
    if status == FriendshipRequest.ACCEPTED:
     friend_Request.save()
     user.friends.add(request.user)
     user.friends_count=user.friends_count+1
     user.save()
     request_user=request.user
     request_user.friends_count=request_user.friends_count+1
     request_user.save()
     notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friend_Request.id)
    elif status == FriendshipRequest.REJECTED:
        # Delete the friendship request and don't add the user as a friend
        friend_Request.delete()
    return JsonResponse({'Job':'done'})
    
@api_view(['POST'])
def editprofile(request):
    user=request.user
    email=request.data.get('email')
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message':'email already exists'})
    else:
        print(request.POST)
        print(request.FILES)
        form=ProfileForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
        serializer=UserSerailzier(user)
        return JsonResponse({'message':'information updated','user':serializer.data})
    
@api_view(['POST'])
def editpassword(request):
    user=request.user
    form = PasswordChangeForm(data=request.data,user=user)
    if form.is_valid():
        form.save()
        return JsonResponse({'message':'success'})
    else:
        message = form.errors.as_json()
        #message='error'
        print(message)
        return JsonResponse({'message': message}, safe=False)
    
@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerailzier(request.user.people_you_may_know.all(), many=True)

    return JsonResponse(serializer.data, safe=False)