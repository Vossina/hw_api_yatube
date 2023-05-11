from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(null=True, default=None, upload_to='posts/image/')
    group = models.ForeignKey(Group, related_name='posts', 
                              blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.author}, {self.text}'
    
class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments',on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.post}, {self.author}, {self.text}'

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='self_user', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follow', on_delete=models.CASCADE)    

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user','following'], name="unique_followers")
    #     ]

    def __str__(self) -> str:
        return f'{self.user} follows {self.following}'
