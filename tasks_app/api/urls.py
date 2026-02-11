from django.urls import path
from .views import (
    TaskAssignedToMeView,
    TaskReviewingView, 
    TaskCreateView,
    TaskDetailView,
    TaskCommentsView,
    CommentDetailView
)

urlpatterns = [
    path('tasks/assigned-to-me/', TaskAssignedToMeView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing/', TaskReviewingView.as_view(), name='tasks-reviewing'),
    path('tasks/', TaskCreateView.as_view(), name='tasks-create'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='tasks-detail'),
    path('tasks/<int:task_id>/comments/', TaskCommentsView.as_view(), name='task-comments'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
]
