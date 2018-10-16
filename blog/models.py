from django.db import models
# 专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible


# Create your models here.

# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
# 分类数据库表
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 标签数据库
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章数据库
@python_2_unicode_compatible
class Post(models.Model):
    '''
    文章数据库包含字段：标题title 正文body  创建时间created_time
    修改时间modified_time 摘要excerpt  分类category 标签tag 作者author
    '''
    title = models.CharField(max_length=100)

    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()

    created_time = models.DateTimeField()

    modified_time = models.DateTimeField()

    # blank 为true表示参数可以为空值za
    excerpt = models.CharField(max_length=200, blank=True)

    # ForeignKey，即一对多的关联关系(一个分类下可以有多篇文章)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，
    # 所以我们使用 ManyToManyField，表明这是多对多的关联关系。文章可以没有标签，所以blank可以为true
    tag = models.ForeignKey(Tag, blank=True, on_delete=models.CASCADE)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，
    # User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 阅读数（>0的数）
    views = models.PositiveIntegerField(default=0)

    # 增加阅读数的方法
    def increase_views(self):
        self.views += 1
        # update_fields 只更新数据库中的views
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        # ordering 用来指定文章排序，
        ordering = ['-created_time']
