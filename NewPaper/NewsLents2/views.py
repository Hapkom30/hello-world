from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm, StateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

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
    permission_required = ('NewsLents2.create_post',)
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