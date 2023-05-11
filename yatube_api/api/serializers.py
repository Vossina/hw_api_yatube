import base64
from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from posts.models import User, Post, Group, Comment, Follow
from djoser.serializers import UserSerializer

class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')



class PostSerializer(serializers.ModelSerializer):
    # group = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    image = Base64ImageField(required=False, allow_null=True)
    author = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')

    # def update(self, instance, validated_data):
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.group = validated_data.get('group', instance.group)
        
    #     instance.save()
    #     return instance

# class UserSerializer(serializers.ModelSerializer):
#     posts = PostSerializer(many=True, required=False)
#     following = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'posts', 'following')
    
    # def get_following(self, obj):
    #     return FollowSerializer(obj.following.all(), many=True).data

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'post', 'created')
        read_only_fields = ('post',)

    # def update(self, instance, validated_data):
    #     instance.text = validated_data.get('text', instance.text)
    #     instance.save()
    #     return instance


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True, default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all())
    
    class Meta:
        model = Follow
        fields = ('user', 'following')

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=('user', 'following'),
        #         message='На себя подписываться нельзя'
        #     )
        # ]