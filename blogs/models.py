from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category-posts', kwargs={'slug': self.slug})

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(max_length=300)
    content = CKEditor5Field('Content', config_name='extends')
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='blog_posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(help_text="Read time in minutes")
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['published_date']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Contact(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('website', 'Website Development'),
        ('mobile', 'Mobile App'),
        ('ecommerce', 'E-commerce Store'),
        ('consultation', 'IT Consultation'),
        ('other', 'Other'),
    ]

    BUDGET_CHOICES = [
        ('5k-15k', '₹5,000 - ₹15,000'),
        ('15k-30k', '₹15,000 - ₹30,000'),
        ('30k-50k', '₹30,000 - ₹50,000'),
        ('50k+', '₹50,000+'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True, null=True)
    project_type = models.CharField(max_length=30, choices=PROJECT_TYPE_CHOICES, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    


class JobNotification(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('FRESHER', 'Fresher'),
        ('EXPERIENCED', 'Experienced'),
        ('ALL', 'All Levels'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='ALL')
    posted_on = models.DateField(auto_now_add=True)
    last_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends')
    requirements = CKEditor5Field('Requirements', config_name='extends')
    apply_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f"{self.title} at {self.company}"
