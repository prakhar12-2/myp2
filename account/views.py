from django.shortcuts import render
from django.http import HttpResponse
from .models import User
def activateaccount(request):
    email=request.GET.get('email','')
    id=request.GET.get('id','')
    
    if email and id:
        user=User.objects.get(id=id,email=email)
        user.is_active=True
        user.save()
        return HttpResponse('The user is activated please move to login page')
    else:
        return HttpResponse('Something went wrong')

