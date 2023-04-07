from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utls import _add_paginator_page


class IndexHome(ListView):
    """Домашния страница"""
    model = Post
    template_name = 'posts/index.html'
    paginate_by = settings.COUNT_POST_PAGE

    @method_decorator(cache_page(settings.CACHE_TIME, key_prefix='index_page'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class GroupPosts(ListView):
    """Страница для групп"""
    model = Post
    template_name = 'posts/group_list.html'
    paginate_by = settings.COUNT_POST_PAGE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.filter(slug=self.kwargs['slug'])[0]
        return context

    def get_queryset(self):
        return Post.objects.filter(group__slug=self.kwargs['slug'])


class Profile(LoginRequiredMixin, ListView):
    """
    View-класс для отображения страницы профиля пользователя.
    """

    model = Post
    template_name = 'posts/profile.html'
    paginate_by = settings.COUNT_POST_PAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        following = (
            self.request.user.is_authenticated and Follow.objects.filter(
                    user=self.request.user,
                    author=author).exists()
                )
        context.update({
            'author': author,
            'following': following,
            'post_author': author.post.all(),
        })
        return context

    def get_queryset(self):
        """
        Возвращает список постов, связанных с автором,
        чей профиль отображается на странице.
        """
        author = get_object_or_404(User, username=self.kwargs['username'])
        return author.post.all()


class PostDetailView(DetailView, LoginRequiredMixin):
    """
    View-класс для отображения страницы с детальной информацией о посте.
    модель Django, используемая для получения данных поста.
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        """
        возвращает словарь контекста для шаблона страницы поста,
        который содержит информацию о количестве постов автора,
        комментарии к посту и форму для добавления нового комментария.
        """

        context = super().get_context_data(**kwargs)
        post_author_id = self.object.author.post.count()
        comments = self.object.comments.all()
        form = CommentForm()
        context.update({
            'count_post_author': post_author_id,
            'form': form,
            'comments': comments,
        })
        return context

    def post(self, request, *args, **kwargs):
        """
        обрабатывает POST-запрос на добавление нового комментария к посту.
        Если данные формы валидны, то создает новый объект Comment,
        связанный с текущим постом и авторизованным пользователем,
        сохраняет его в базе данных и перенаправляет пользователя на стран
        ицу с детальной информацией о посте.
        Если данные формы невалидны,
        то возвращает страницу с детальной информацией о постес указанием ошибок в форме
        """
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('posts:post_detail', post_id=self.kwargs['pk'])
        return self.render_to_response(self.get_context_data(form=form))



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
