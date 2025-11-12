from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('blog-posts/', views.BlogPostListView.as_view(), name='blog-list'),
    path('blog-posts/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('contact/', views.ContactCreateView.as_view, name='contact-create'),
]
