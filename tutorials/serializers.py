from rest_framework import serializers
from .models import Tutorial, Topic, Comment, TopicReaction

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
    class Meta:
        model = Topic
        fields = ['id', 'title', 'slug']  # only ID & title


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
    topics = TopicTitleSerializer(many=True, read_only=True)
    total_topics = serializers.SerializerMethodField()

    class Meta:
        model = Tutorial
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'total_topics',
            'topics'
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
