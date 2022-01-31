from account.models import User
from django.urls import reverse
from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

#My Managers
class PostManager(models.Manager):
    def published(self):
        return self.filter(status="p")

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# My Models
class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name="child", verbose_name="زیر دسته")
    title = models.CharField(max_length=100, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name="نمایش داده شود؟")
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')

class Post(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشرشده'),
        ('i', 'درحال بررسی'),
        ('b', 'رد شده'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="postauthor", verbose_name="نویسنده")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="آدرس پست")
    category = models.ManyToManyField(Category, verbose_name="دسته بندی", related_name="postcat")
    content = models.TextField(verbose_name="محتویات پست")
    thumbnail = models.ImageField(upload_to="images", verbose_name="تصویر کاور")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    is_special = models.BooleanField(default=False, verbose_name="پست ویژه")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت انتشار")
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, blank=True, through='PostHit', related_name='hits', verbose_name='بازدیدها')

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        ordering = ['-publish']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("account:home")
    

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def jupdated(self):
        return jalali_converter(self.updated)
    jupdated.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'".format(self.thumbnail.url))
    thumbnail_tag.short_description = "تصویر"

    def category_to_str(self):
            return "، ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته بندی"

    objects = PostManager()


class PostHit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)