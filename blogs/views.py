from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy, reverse
from accounts.models import CustomUser
from django.shortcuts import redirect, get_object_or_404


class Home(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 6
    def get_queryset(self):
        user = self.request.user
        user_groups = user.group_memberships.all()
        return Post.objects.filter(author__group_memberships__in=user_groups).distinct()

class UserBlog(LoginRequiredMixin, ListView):
    template_name = 'blogs/user_post.html'
    model = Post
    paginate_by = 6
    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return Post.objects.filter(author__id = user_id)
    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context= super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        context['user'] = CustomUser.objects.get(id=user_id)
        return context

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blogs/create_post.html'
    fields = ['title', 'image', 'content']
    success_url = reverse_lazy('blogs:home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, pk=kwargs['pk'])
        if self.object.slug != kwargs.get('slug'):
            return redirect('blogs:post_detail', pk=self.object.pk, slug=self.object.slug)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blogs/edit_post.html'
    fields = ['title', 'image', 'content']
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    def get_success_url(self):
        return reverse('blogs:post_detail', kwargs={'pk':self.object.pk, 'slug':self.object.slug})

class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blogs:home')