from django.contrib import admin
from . models import Post, Comment, Message, Friend, Notification

# Register models for admin

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Notification)
