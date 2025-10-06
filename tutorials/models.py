from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

User = settings.AUTH_USER_MODEL


class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field('Text', config_name='extends')
    thumbnail = models.ImageField(upload_to='tutorial_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_topics(self):
        return self.topics.count()

    def save(self, *args, **kwargs):
        if not self.slug:  # Auto-generate only on create
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Tutorial.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Topic(models.Model):
    tutorial = models.ForeignKey(Tutorial, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = CKEditor5Field('Text', config_name='extends')
    video_url = models.URLField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Topic.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tutorial.title} - {self.title}"


class Comment(models.Model):
    topic = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return f"{self.user.username} on {self.topic.title}"


class TopicReaction(models.Model):
    topic = models.ForeignKey(Topic, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='topic_reactions', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('topic', 'user')


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.SET_NULL)
    activity_type = models.CharField(max_length=50, choices=[
        ('comment', 'Commented'),
        ('like', 'Liked'),
        ('dislike', 'Disliked'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
