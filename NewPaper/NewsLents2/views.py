from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Post, Category, PostCategory, Subscription
from .filters import PostFilter
from .forms import PostForm, StateForm

from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)



class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    logger.info('INFO')

    def get_queryset(self):
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['category'] = Category.objects.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['postcategory'] = PostCategory.objects.all()
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsLents2.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsLents2.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsLents2.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class StateCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsLents2.add_post',)
    form_class = StateForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_or_state = True
        return super().form_valid(form)

class StateEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsLents2.change_post',)
    form_class = StateForm
    model = Post
    template_name = 'post_edit.html'

class StateDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsLents2.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user,category=category).delete()

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk')))).order_by('category')

    return render(request,'subscriptions.html',{'categories': categories_with_subscriptions})
