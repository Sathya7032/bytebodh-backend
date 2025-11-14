from rest_framework import serializers
from .models import Category, Tag, BlogPost, Contact, JobNotification

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    author = serializers.StringRelatedField()
    published_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'excerpt', 'content', 'featured_image', 'category', 'tags', 'author', 'status', 'views', 'read_time', 'published_date', 'created_at', 'updated_at', 'is_featured']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class JobNotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobNotification
        fields = ['id', 'title', 'company', 'location', 'experience_level', 'posted_on', 'last_date']

class JobNotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobNotification
        fields = '__all__'  # Show all details in detailed view