from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from posts.models import User, Post, Group, Comment, Follow
from .permissions import AuthorOrReadOnly, ReadOnly
from .serializers import PostSerializer, CustomUserSerializer, GroupSerializer, CommentSerializer, FollowSerializer
from django.shortcuts import get_object_or_404
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_permissions(self):
    # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
        # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()
    
    def perform_create(self, serializer):       # эта штука позволила постить посты без автора хотя в get он высвечивается
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = None


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None

    def get_permissions(self):      # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = None

    def get_permissions(self):      # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_permissions(self):      # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):       # эта штука позволила постить посты без автора хотя в get он высвечивается
        serializer.save(user=self.request.user)пше