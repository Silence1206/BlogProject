from django import template
from ..models import Post,Category


# 注册模板
register = template.Library()

#1. 最新模板：查找最新的五条文章(装饰)
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

#2. 归档模板：精确到月份降序排序
@register.simple_tag
def archives():
    return Post.objects.all().dates('created_time','month',order='DESC')

#3. 分类模板
@register.simple_tag
def get_categories():
    return Category.objects.all()