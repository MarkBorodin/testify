from django.contrib import admin

from .models import Client, Comment, Lessons, Level, Post


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Level)
admin.site.register(Client)
admin.site.register(Lessons)
