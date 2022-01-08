from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import serializer_helpers
from .serializers import TaskSerializer, UserSerializer, EmailVerificationSerializer
from .models import Task, User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings

# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list',
        'Detail View': '/task-detail/<str:pk>',
        'Create': '/task-create',
        'Update': '/task-update/<str:pk>',
        'Delete': '/task-delete/<str:pk>',
        'UserList': "/user-list",
        'UserDetail': '/user-detail/<str:email>',
        'UserCreate': '/user-create/',
        'UserUpdate': '/user-update/<str:email>',
        'UserDelete': '/user-delete/<str:email>',
    }
    return Response(api_urls)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.object.get(id=pk)
    task.delete()
    return Response("Item successfully deleted!")


@api_view(['GET'])
def userList(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def userDetail(request, email):
    users = User.objects.get(email=email)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def userCreate(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    user_data = serializer.data
    user = User.objects.get(email=user_data['email'])
    token = RefreshToken.for_user(user).access_token

    # current_site = get_current_site(request).domain
    current_site = 'localhost:3000/email-verify/'

    # relativeLink = reverse('email-verify')

    # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
    absurl = 'http://'+current_site+"token="+str(token)

    email_body = 'Hello. Use link below to verify your email \n' + absurl
    data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'}
    Util.send_email(data)
    return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            new_joinne = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=new_joinne['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated!'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Link expired!'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def userUpdate(request, email):
    user = User.objects.get(email=email)
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def userDelete(request, email):
    user = User.objects.get(email=email)
    user.delete()
    return Response("User successfully deleted!")
