"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.shortcuts import render, redirect
import fake_db
from todo import views
from users import views as users_views

def index(request):
    return redirect('login')
def user_list(request):
    user_index = list(fake_db.user_db.keys())
    print(user_index)

    users = [(index, fake_db.user_db[index]['이름']) for index in user_index] # 튜플로 전달
    print(users)

    return render(request, 'user_list.html', {'users':users})

def user_info(request, user_id):
    user = fake_db.user_db[user_id]
    print(user)

    return render(request, 'user_info.html', {'user':user})

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),

    # author
    path('users/', user_list),
    path('users/<int:user_id>/', user_info),
    path('accounts/', include("django.contrib.auth.urls")), # logout을 위한 라인
    path('login/', users_views.login, name='login'),
    path('signup/', users_views.signup, name='signup'),

    # todo
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>/', views.todo_info, name='todo_info'),
    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/<int:todo_id>/update/', views.todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),
]
