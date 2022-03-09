from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskView.as_view(), name='tasks'),
    path('tasks/<int:pk>', views.TaskDetail.as_view(), name='task'),
    path('tasks/add/', views.CreateTask.as_view(), name='task-create'),
    path('tasks/delete/<int:pk>/', views.DeleteTask.as_view(), name='task-delete'),
    path('tasks/edit/<int:pk>/', views.EditTask.as_view(), name='task-edit'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home')
]