from django.db import models

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField(max_length=255)

    url = models.URLField(blank=True)

    text = models.TextField()

    #自动生成评论时间

    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post',on_delete=None)

    def __str__(self):
        return self.text[:20]