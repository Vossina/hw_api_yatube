from django.contrib import admin
from .models import Group, Post, Comment, Follow

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'pub_date', 'image', 'group')
    search_fields = ['author']
    list_filter = ['pub_date']


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'description')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'text', 'created')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
