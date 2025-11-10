from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Tutorial, Topic, Comment, TopicReaction
from .serializers import *


# ======================
# Tutorials (READ ONLY but Auth Required)
# ======================

class TutorialListView(generics.ListAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialListSerializer
    permission_classes = [permissions.IsAuthenticated]  # login required


class TutorialDetailView(generics.RetrieveAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialDetailSerializer
    permission_classes = [permissions.IsAuthenticated]  # login required
    lookup_field = "slug"


# ======================
# Topics (READ ONLY but Auth Required)
# ======================

class TopicListView(generics.ListAPIView):
    serializer_class = TopicTitleSerializer
    permission_classes = [permissions.IsAuthenticated]  # login required

    def get_queryset(self):
        tutorial_slug = self.kwargs['tutorial_slug']
        return Topic.objects.filter(tutorial__slug=tutorial_slug)


class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]  # login required
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# ======================
# Comments (CRUD - Auth Required)
# ======================

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # login required

    def get_queryset(self):
        topic_slug = self.kwargs['topic_slug']
        return Comment.objects.filter(topic__slug=topic_slug)

    def perform_create(self, serializer):
        topic_slug = self.kwargs['topic_slug']
        topic = get_object_or_404(Topic, slug=topic_slug)
        serializer.save(user=self.request.user, topic=topic)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # login required

    def get_queryset(self):
        return Comment.objects.all()

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionError("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError("You can only delete your own comments.")
        instance.delete()


# ======================
# Comment Like / Dislike (Auth Required)
# ======================

class CommentReactionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # login required

    def post(self, request, comment_id):
        action = request.data.get('action')
        comment = get_object_or_404(Comment, id=comment_id)

        if action == "like":
            comment.likes.add(request.user)
            comment.dislikes.remove(request.user)
        elif action == "dislike":
            comment.dislikes.add(request.user)
            comment.likes.remove(request.user)
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


# ======================
# Topic Like / Dislike (Auth Required)
# ======================

class TopicReactionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, topic_slug):
        action = request.data.get('action')
        topic = get_object_or_404(Topic, slug=topic_slug)

        # Ensure the reaction exists (default is_like=False)
        reaction, _ = TopicReaction.objects.get_or_create(
            topic=topic,
            user=request.user,
            defaults={"is_like": False}
        )

        if action == "like":
            reaction.is_like = True
        elif action == "dislike":
            reaction.is_like = False
        else:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        reaction.save()

        return Response({
            "likes": topic.reactions.filter(is_like=True).count(),
            "dislikes": topic.reactions.filter(is_like=False).count()
        })


class MyCommentsView(generics.ListAPIView):
    serializer_class = UserCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user).order_by('-created_at')

class ProblemListView(generics.ListAPIView):
    """
    List all problems under a given topic.
    """
    serializer_class = ProblemListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        topic_slug = self.kwargs.get('topic_slug')
        return Problems.objects.filter(topic__slug=topic_slug).order_by('-created_at')


class ProblemDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a specific problem by slug.
    """
    queryset = Problems.objects.all()
    serializer_class = ProblemDetailSerializer
    lookup_field = 'slug'

class ProblemsListAPIView(generics.ListAPIView):
    queryset = Problems.objects.select_related('topic', 'topic__tutorial').all()
    serializer_class = ProblemsSerializer