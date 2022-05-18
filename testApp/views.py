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
import datetime as dt
# from summarizer import Summarizer
# Create your views here.

# model = Summarizer()
from transformers import pipeline
summarizer = pipeline(
    "summarization", model="philschmid/distilbart-cnn-12-6-samsum")


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


def give_time(transcript):
    startPM = transcript.find("PM:")
    startAM = transcript.find("AM:")
    if(startAM != -1 and startPM != -1):
        start = min(startAM, startPM)
    elif(startAM == -1 and startPM != -1):
        start = startPM
    else:
        start = startAM
    string = transcript[start - 10:start + 3]
    dash = string.find("-")
    string = string[dash + 1:]
    EM = string.find("M")
    start = string[1:EM + 1]
    # print(start)
    PM = transcript.rfind("PM:")
    AM = transcript.rfind("AM:")
    if(AM > PM):
        end = AM
    else:
        end = PM
    string = transcript[end - 10:end + 3]
    dash = string.find("-")
    string = string[dash + 1:]
    EM = string.find("M")
    end = string[1:EM + 1]
    # print(end)
    if(start[len(start) - 2:] == "PM"):
        colon = start.find(":")
        start = str(int(start[:colon]) + 12) + start[colon:-3] + ":00"
    else:
        start = start[:-3] + ":00"
    if(end[len(end) - 2:] == "PM"):
        colon = end.find(":")
        end = str(int(end[:colon]) + 12) + end[colon:-3] + ":00"
    else:
        end = end[:-3] + ":00"
    start_dt = dt.datetime.strptime(start, "%H:%M:%S")
    end_dt = dt.datetime.strptime(end, "%H:%M:%S")
    duration = end_dt - start_dt
    return str(duration)


def Attendance(transcript):
    names = set()
    for line in transcript.split('\n'):
        if "PM:" in line:
            dash = line.find("-")
            name = line[:dash - 1]
            names.add(name)
        elif "AM:" in line:
            dash = line.find("-")
            name = line[:dash - 1]
            names.add(name)
    return [len(names), names]


@api_view(['POST'])
def userTextData(request):
    # print(request.data)
    time_duration = give_time(request.data['article'])
    speakers = Attendance(request.data['article'])
    summary = mlFunction(request.data['article'])
    return Response({"summary": summary, "time_duration": time_duration, "totalSpeakers": speakers[0], "speakerNames": speakers[1]}, status=status.HTTP_201_CREATED)
    # return Response(request.data["article"])


def mlFunction(text):
    # print("This is working ", text)
    summary = summarizer(text)
    return summary


@api_view(['POST'])
def sendSummaryEmail(request):
    email_body = 'Hello. This is the summary generated of the meet. \n\n' + \
        request.data['summary']
    # email_body = 'Hello. This is the summary generated of the meet. \n\n' + \
    #     request.data['summary']+'\n\n Time duration of the meet: ' + request.data['time_duration'] + '\n\n Total Speakers: ' + request.data['totalSpeakers'] + '\n\n Speakers: ' + request.data['speakerNames'] 
    to_email = request.data['send_to']
    print(to_email)
    data = {'email_body': email_body, 'to_email': to_email,
            'email_subject': 'Meet Summary'}
    Util.send_email(data)
    return Response("Meet summary mail sent!", status=status.HTTP_201_CREATED)
