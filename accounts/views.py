from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import CustomUser
from django.contrib.auth.views import LoginView
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import UserEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class SignUpView(CreateView):
    model = CustomUser
    template_name = 'accounts/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('blogs:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return redirect(next_url)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return reverse_lazy('blogs:home')

class UserEditView(LoginRequiredMixin ,UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('blogs:home')
    def get_object(self, queryset = None):
        return self.request.user


@login_required
def delete_image(request, pk):
    print('hi')
    try:
        user = CustomUser.objects.get(id=pk)
        if user.profile_image.name != 'profiles/default_profile.png':
            user.profile_image.delete()
            return JsonResponse({'response': 'delete'})
    except:
        return JsonResponse({'response': 'not_found'})
