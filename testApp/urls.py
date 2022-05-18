from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('task-list/', views.taskList, name="task-list"),
    path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
    path('task-create/', views.taskCreate, name="task-create"),
    path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
    path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
    path('user-list/', views.userList, name="user-list"),
    path('user-detail/<str:email>/', views.userDetail, name="user-detail"),
    path('user-create/', views.userCreate, name="user-create"),
    path('user-update/<str:email>/', views.userUpdate, name="user-update"),
    path('user-delete/<str:email>/', views.userDelete, name="user-delete"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('user-data/',views.userTextData, name="user-data"),
    path('send-summary/',views.sendSummaryEmail, name="send-summary"),
]
