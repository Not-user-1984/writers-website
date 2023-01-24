from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utls import _add_paginator_page


# @cache_page(settings.CACHE_TIME, key_prefix='index_page')
class IndexHome(ListView):
    """Домашния страница"""
    model = Post
    template_name = 'posts/index.html'
    paginate_by = settings.COUNT_POST_PAGE


# @cache_page(settings.CACHE_TIME, key_prefix='index_page')
# def index(request):
#     """ the main page of the yatube website"""
#     posts = (
#         Post.objects
#         .select_related('group').all()
#     )
#     page_obj = _add_paginator_page(request, posts)
#     context = {
#         'page_obj': page_obj,
#     }
#     return render(request, 'posts/index.html', context)

class GroupPosts(ListView):
    """Страница для групп"""
    model = Post
    template_name = 'posts/group_list.html'
    paginate_by = settings.COUNT_POST_PAGE

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.filter(slug=self.kwargs['slug'])[0]
        return context

    def get_queryset(self):
        return Post.objects.filter(group__slug=self.kwargs['slug'])


# def group_posts(request, slug):
#     """the page of the group of posts"""
#     group = get_object_or_404(Group, slug=slug)
#     posts = group.groups.all()
#     page_obj = _add_paginator_page(request, posts)
#     context = {
#         'group': group,
#         'page_obj': page_obj,
#     }
#     return render(request, 'posts/group_list.html', context)


class Profile(ListView):
    """страница профиля"""
    # queryset = Post.objects.filter(author__username=kwargs['username'])
    model = Post
    template_name = 'posts/profile.html'
    paginate_by = settings.COUNT_POST_PAGE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(
            User, username=self.kwargs['username']
            )
        context['following'] = (
                self.request.user.is_authenticated
                and Follow.objects.filter(
                        user=self.request.user,
                        author=context['author']).exists()
        )
        context['post_author'] = context['author'].post.all()
        return context

    def get_queryset(self):
        return Post.objects.filter(author__username=self.kwargs['username'])



# def profile(request, username):
#     """"the user's page and his posts"""
#     author = get_object_or_404(User, username=username)
#     post_author = author.post.all()
#     page_obj = _add_paginator_page(request, post_author)
#     following = (
#             request.user.is_authenticated
#             and Follow.objects.filter(
#         user=request.user, author=author
#     ).exists()
#     )
#     context = {
#         'author': author,
#         'post_author': post_author,
#         'page_obj': page_obj,
#         'following': following,
#     }
#     return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """страница отдельного поста"""
    post_detail_id = get_object_or_404(Post, pk=post_id)
    comments = post_detail_id.comments.all()
    form = CommentForm(request.POST or None)
    post_author_id = post_detail_id.author.post.count()
    context = {
        'post': post_detail_id,
        'count_post_author': post_author_id,
        'form': form,
        'comments': comments,
    }
    return render(
        request,
        'posts/post_detail.html',
        context
    )


@login_required
def post_create(request):
    """форма для создания поста"""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect(
            'posts:profile',
            username=form.author
        )
    return render(
        request,
        'posts/create_post.html',
        {'form': form}
    )


@login_required
def post_edit(request, post_id):
    """форма для редактирование поста"""
    is_edit = get_object_or_404(Post, id=post_id, author=request.user)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=is_edit
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=is_edit.id)
    context = {
        'form': form,
        'is_edit': is_edit
    }
    return render(
        request,
        'posts/create_post.html',
        context
    )


@login_required
def add_comment(request, post_id):
    """форма для создания комментария"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """делает подписку на автора """
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = _add_paginator_page(request, post_list)
    return render(
        request,
        'posts/follow.html',
        {'page_obj': page_obj}
    )


@login_required
def profile_follow(request, username):
    """Показывает посты подписок"""
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect(
        'posts:profile',
        username=username
    )


@login_required
def profile_unfollow(request, username):
    """отписка от автора"""
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect(
        'posts:profile',
        username=username
    )
