from django.contrib import admin
from .models import *

# ======================
# Tutorial Admin
# ======================
@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_topics', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}  # Auto slug generation
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'description', 'thumbnail')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def total_topics(self, obj):
        return obj.topics.count()
    total_topics.short_description = 'Topics Count'


# ======================
# Topic Admin
# ======================
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutorial', 'views', 'created_at')
    search_fields = ('title', 'tutorial__title')
    list_filter = ('tutorial', 'created_at')
    readonly_fields = ('views', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}  # Auto slug generation
    ordering = ('-created_at',)
    fieldsets = (
        ('Topic Info', {
            'fields': ('tutorial', 'title', 'slug', 'content', 'video_url')
        }),
        ('Statistics', {
            'fields': ('views',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


# ======================
# Comment Admin
# ======================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'content', 'total_likes', 'total_dislikes', 'created_at')
    search_fields = ('user__username', 'topic__title', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Comment Info', {
            'fields': ('user', 'topic', 'content', 'likes', 'dislikes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def total_likes(self, obj):
        return obj.likes.count()
    total_likes.short_description = 'Likes'

    def total_dislikes(self, obj):
        return obj.dislikes.count()
    total_dislikes.short_description = 'Dislikes'


# ======================
# Topic Reaction Admin
# ======================
@admin.register(TopicReaction)
class TopicReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'is_like')
    search_fields = ('user__username', 'topic__title')
    list_filter = ('is_like',)
    ordering = ('user',)

from django.utils.safestring import mark_safe


class ProblemsAdmin(admin.ModelAdmin):
    list_display = ( 'topic','title', 'created_at', 'updated_at')
    search_fields = ('question', 'code_snippet')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)} 

    # To make the code snippet more readable in the admin
    def code_snippet_display(self, obj):
        return mark_safe(f"<pre><code>{obj.code_snippet}</code></pre>" if obj.code_snippet else "No code")
    code_snippet_display.short_description = 'Code Snippet'
    
    # Displaying the video URL in the admin panel
    def video_embed(self, obj):
        if obj.video_url:
            return mark_safe(f'<a href="{obj.video_url}" target="_blank">Watch Video</a>')
        return "No video"
    video_embed.short_description = 'Video Link'
    
    # Fields to display in the form view
    fieldsets = (
        (None, {
            'fields': ('topic','title','slug', 'question', 'code_snippet', 'explanation', 'video_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    # Optionally, you could add a rich text widget for the code snippet if needed
    # You can also configure `CKEditor` here if you want to use it for the code snippet too

admin.site.register(Problems, ProblemsAdmin)


# ======================
# Admin Branding
# ======================
admin.site.site_header = "🎓 Tutorials Admin Dashboard"
admin.site.site_title = "Tutorial Management Portal"
admin.site.index_title = "Welcome to the Learning Platform Admin"
