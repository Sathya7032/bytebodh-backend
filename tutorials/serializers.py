from rest_framework import serializers
from .models import Tutorial, Topic, Comment, TopicReaction, Problems

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    total_dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'total_likes',
            'total_dislikes',
            'created_at',
            'updated_at'
        ]


class TopicSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'tutorial', 'title', 'content', 'video_url', 'views', 'created_at', 'updated_at', 'comments', 'reactions']

    def get_reactions(self, obj):
        likes = obj.reactions.filter(is_like=True).count()
        dislikes = obj.reactions.filter(is_like=False).count()
        return {'likes': likes, 'dislikes': dislikes}



class TopicTitleSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'slug', 'views', 'likes', 'dislikes']  # Replacing reactions with likes and dislikes

    def get_likes(self, obj):
        # Count the number of likes (assuming `is_like=True` represents a like)
        return obj.reactions.filter(is_like=True).count()

    def get_dislikes(self, obj):
        # Count the number of dislikes (assuming `is_like=False` represents a dislike)
        return obj.reactions.filter(is_like=False).count()


class TutorialSerializer(serializers.ModelSerializer):
    topics = TopicTitleSerializer(many=True, read_only=True)
    total_topics = serializers.SerializerMethodField()

    class Meta:
        model = Tutorial
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'created_at',
            'updated_at',
            'topics',
            'total_topics',
            'slug'
        ]

    def get_total_topics(self, obj):
        return obj.topics.count() if obj.topics.exists() else 0

class TutorialListSerializer(serializers.ModelSerializer):
    # topics = TopicTitleSerializer(many=True, read_only=True)
    total_topics = serializers.SerializerMethodField()

    class Meta:
        model = Tutorial
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'total_topics',
            'slug',
            'created_at',
        ]

    def get_total_topics(self, obj):
        return obj.topics.count()

class TutorialDetailSerializer(serializers.ModelSerializer):
    topics = TopicTitleSerializer(many=True, read_only=True)
    total_topics = serializers.SerializerMethodField()

    class Meta:
        model = Tutorial
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'created_at',
            'updated_at',
            'topics',
            'total_topics'
        ]

    def get_total_topics(self, obj):
        return obj.topics.count()

class UserCommentSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    total_dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'topic_title', 'content', 'total_likes', 'total_dislikes', 'created_at']

class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ['title', 'slug']


class ProblemDetailSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField()  # Shows topic title instead of ID

    class Meta:
        model = Problems
        fields = [
            'id',
            'topic',
            'title',
            'slug',
            'question',
            'code_snippet',
            'explanation',
            'video_url',
            'created_at',
            'updated_at'
        ]

#Problem Serializer start here

class ProblemsSerializer(serializers.ModelSerializer):
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    tutorial_title = serializers.CharField(source='topic.tutorial.title', read_only=True)

    class Meta:
        model = Problems
        fields = [
            'id',
            'title',
            'slug',
            'topic_title',
            'tutorial_title',
            'created_at',
            'updated_at'
        ]