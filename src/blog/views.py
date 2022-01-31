from .models import Post, Category
from django.views.generic import ListView, DetailView
from account.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from account.mixins import AuthorAccessMixin
from django.db.models import Q


class HomePosts(ListView):
    queryset = Post.objects.published()
    paginate_by = 6



class PostDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in post.hits.all():
            post.hits.add(ip_address)
        return post



class PostPreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=pk)


class CategoryList(ListView):
    paginate_by = 6
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.postcat.published()

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['category'] = category
            return context


class AuthorList(ListView):
    paginate_by = 4
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.postauthor.published()

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['author'] = author
            return context


class SearchList(ListView):
    paginate_by = 4
    template_name = 'blog/search_list.html'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Post.objects.filter(Q(content__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['search'] = self.request.GET.get('q')
            return context