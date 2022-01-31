from django import template
from ..models import Category
from ..models import Post
from django.db.models import Count, Q
from datetime import datetime, timedelta

register = template.Library()

@register.simple_tag
def blog_title():
    return "گیک لاگ"

@register.inclusion_tag("blog/partials/category_home.html")
def category_home():
    return {
        "category": Category.objects.filter(status=True)
    }

@register.inclusion_tag("blog/partials/category_nav.html")
def category_nav():
    return {
        "category": Category.objects.filter(status=True)
    }

@register.inclusion_tag("registration/partials/active_link.html")
def active_link(request, link_name, content, classes):
    return {
        "request": request,
        "link_name": link_name,
        "link": "account:{}".format(link_name),
        "content": content,
        "classes": classes,
    }

@register.inclusion_tag("blog/partials/sidebar_posts.html")
def popular_posts():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "posts": Post.objects.published().annotate(count=Count('hits', filter=Q(posthit__created__gt=last_month))).order_by('-count', '-publish')[:5],
        "title": "پربازدید ترین ها (ماه)"
    }

@register.inclusion_tag("blog/partials/sidebar_posts.html")
def hot_posts():
    last_month = datetime.today() - timedelta(days=30)
    return {
        "posts": Post.objects.published().annotate(count=Count('hits', filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=6))).order_by('-count', '-publish')[:5],
        "title": "داغ ترین ها (ماه)"
    }