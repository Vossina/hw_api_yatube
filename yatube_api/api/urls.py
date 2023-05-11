from rest_framework import routers
from django.urls import path, include
from .views import UserViewSet, PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = routers.DefaultRouter()

router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'users', UserViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', 
                CommentViewSet, basename='comments')
router.register('follow', FollowViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
