from django.contrib import admin

from .models import Client, Comment, Contact, Lessons, Level, Post, Whose


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Level)
admin.site.register(Client)
admin.site.register(Whose)
admin.site.register(Lessons)
