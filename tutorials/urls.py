from django.urls import path
from .views import (
    TutorialListView, TutorialDetailView,
    TopicListView, TopicDetailView,
    CommentListCreateView, CommentDetailView,
    CommentReactionView, TopicReactionView, MyCommentsView,
    ProblemListView, ProblemDetailView, ProblemsListAPIView,
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
    path('my-comments/', MyCommentsView.as_view(), name='my-comments'),

    path('topics/<slug:topic_slug>/problems/', ProblemListView.as_view(), name='problem-list'),
    path('problems/<slug:slug>/', ProblemDetailView.as_view(), name='problem-detail'),

    path('all/problems/', ProblemsListAPIView.as_view(), name='problems-list'),

]
