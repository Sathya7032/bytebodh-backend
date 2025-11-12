from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, BlogPost
from .serializers import CategorySerializer, BlogPostSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer

class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        # Get the blog post object
        blog_post = self.get_object()
        
        # Increment the view count for the blog post
        blog_post.increment_views()
        
        # Serialize the blog post data
        serializer = self.get_serializer(blog_post)
        
        # Return the serialized data with a success message
        return Response({
            'message': 'Blog post retrieved and view count incremented successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
