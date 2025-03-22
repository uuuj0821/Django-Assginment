from django.urls import path
from todo import cb_views

app_name = 'todo'

urlpatterns = [
    path('todo/', cb_views.ToDoListView.as_view(), name='list'),
    path('todo/<int:pk>/', cb_views.ToDoDetailView.as_view(), name='info'),
    path('todo/create/', cb_views.ToDoCreateView.as_view(), name='create'),
    path('todo/<int:pk>/update/', cb_views.ToDoUpdateView.as_view(), name='update'),
    path('todo/<int:pk>/delete/', cb_views.ToDoDeleteView.as_view(), name='delete'),
    path('todo/comment/create/<int:pk>/', cb_views.CommentCreateView.as_view(), name='comment_create'),
    path('todo/comment/update/<int:pk>/', cb_views.CommentUpdateView.as_view(), name='comment_update'),
    path('todo/comment/delete/<int:pk>/', cb_views.CommentDeleteView.as_view(), name='comment_delete'),
]
