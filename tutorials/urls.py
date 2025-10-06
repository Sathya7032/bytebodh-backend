from django.urls import path
from .views import (
    TutorialListView, TutorialDetailView,
    TopicListView, TopicDetailView,
    CommentListCreateView, CommentDetailView,
    CommentReactionView, TopicReactionView
)

urlpatterns = [
    path('tutorials/', TutorialListView.as_view(), name='tutorial-list'),
    path('tutorials/<slug:slug>/', TutorialDetailView.as_view(), name='tutorial-detail'),
    path('tutorials/<slug:tutorial_slug>/topics/', TopicListView.as_view(), name='topic-list'),
    path('topics/<slug:slug>/', TopicDetailView.as_view(), name='topic-detail'),
    path('topics/<slug:topic_slug>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:comment_id>/reaction/', CommentReactionView.as_view(), name='comment-reaction'),
    path('topics/<slug:topic_slug>/reaction/', TopicReactionView.as_view(), name='topic-reaction'),
]
