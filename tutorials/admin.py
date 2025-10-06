from django.contrib import admin
from .models import Tutorial, Topic, Comment, TopicReaction
# Register your models here.
admin.site.site_header = "Admin Dashboard"
admin.site.site_title = "Admin Portal"
admin.site.register(Tutorial)
admin.site.register(Topic)  
admin.site.register(Comment)
admin.site.register(TopicReaction)