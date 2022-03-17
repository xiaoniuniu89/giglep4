from django.contrib import admin
from . models import Post, Comment, Message, Friend, Notification, Thread

# Register models for admin

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Thread)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Notification)
