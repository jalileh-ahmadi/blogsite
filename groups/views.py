from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,UpdateView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
import json

from .models import Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import CustomUser
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

class GroupsList(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups/groups_list.html'
    paginate_by = 6
    context_object_name = 'groups'
    def get_queryset(self):
        user = self.request.user
        groups = Group.objects.exclude(admin=user)
        return groups

class UserGroupsList(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups/user_groups_list.html'
    paginate_by = 3
    context_object_name = 'groups'
    def get_queryset(self):
        user = self.request.user
        groups = user.group_memberships.exclude(admin=user)
        return groups
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        userGroups = Group.objects.filter(admin=user)
        page_number = self.request.GET.get('page1')
        paginator = Paginator(userGroups, 3)
        object_list = paginator.get_page(page_number)
        context['usergroups'] = object_list
        return context



@login_required
@require_POST
def add_to_group(request, pk):
    try:
        group = get_object_or_404(Group, id=pk)
        user = request.user
        if user != group.admin:
            if group.member.filter(id=user.id).exists():
                group.member.remove(user)
                return JsonResponse({'status': 'successful_remove'})
            else:
                group.member.add(user)
                return JsonResponse({'status': 'successful_add'})
    except Exception as e:
        return JsonResponse({'status':'unsuccessful', 'error':str(e)})

@login_required
def members_list(request, pk):
    group = Group.objects.get(id=pk)
    members = []
    memberslist = group.member.all()
    for member in memberslist:
        is_admin = False
        if group.admin == member:
            is_admin = True
        members.append(
            {
                'username': member.username,
                'image' : member.profile_image.url,
                'id' : member.id,
                'is_admin' : is_admin
            }
        )
    return JsonResponse({'members':members})

@login_required
@require_POST
def delete_group(request, pk):
    group = get_object_or_404(Group, id=pk)
    if request.user != group.admin:
        messages.error(request, 'شما اجازه حذف گروه را ندارید')
        return redirect('groups:user_groups_list')
    group.delete()
    messages.success(request, "گروه با موفقیت حذف شد.")
    return redirect('groups:user_groups_list')

@login_required
def search_user(request):
    username = request.GET.get('q', '').strip()
    users = CustomUser.objects.filter(username__icontains=username)
    data =[]
    for user in users:
        data.append({
            'id' : user.id,
            'username': user.username,
            'image': user.profile_image.url
        })
    return JsonResponse({'users':data})

@login_required
@require_POST
def add_user_to_group(request, group_id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'خطا در ارسال json'})
    try:
        user_id = data.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        if request.user.id != group.admin_id:
            return JsonResponse({'success': False, 'message': 'فقط ادمین میتواند اضافه کند'})
        if not user_id:
            return JsonResponse({'success': False, 'message': 'شناسه کاربر ارسال نشده است'})
        if group.member.filter(id=user_id).exists():
            return JsonResponse({'success': False, 'message': 'کاربر در گروه عضو است'})
        if not user.allow_group_invites:
            return JsonResponse({'success': False, 'message': 'کاربر به شما اجازه اضافه کردن به گروه را نمیدهد'})
        group.member.add(user)
        return JsonResponse({'success': True})
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'کاربر پیدا نشد'})
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'گروه پیدا نشد'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def search_member(request, pk):
    try:
        username = request.GET.get('q', '').strip()
        group = Group.objects.get(id=pk)
        members = group.member.filter(username__icontains=username)
        data=[]
        for member in members:
            data.append({
                'id' : member.id,
                'username': member.username,
                'image' : member.profile_image.url
            })
        return JsonResponse({'members': data})
    except Exception as e:
        return JsonResponse({'members': [], 'error': str(e)})


@login_required
@require_POST
def remove_member_from_group(request, pk):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'خطا در ارسال json'})
    try:
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'شناسه کاربر ارسال نشده است'})
        group = Group.objects.get(id=pk)
        if request.user.id != group.admin_id:
            return JsonResponse({'success': False, 'message': 'فقط ادمین میتواند حذف کند'})
        user = CustomUser.objects.get(id=user_id)
        if not group.member.filter(id=user_id).exists():
            return JsonResponse({'success': False, 'message': 'کاربر عضو گروه نیست'})
        if request.user == user:
            return JsonResponse({'success': False, 'message': 'ادمین نمیتواند خودش را حذف کند'})
        group.member.remove(user)
        return JsonResponse({'success': True})
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'کاربر پیدا نشد'})
    except Group.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'گروه پیدا نشد'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



class EditGroup(LoginRequiredMixin, UpdateView):
    model = Group
    fields = ['image', 'name']
    template_name = 'groups/edit_group.html'
    success_url = reverse_lazy('groups:user_groups_list')
    def get_queryset(self):
        return Group.objects.filter(admin=self.request.user)

class CreateGroup(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'groups/create_group.html'
    fields = ['name', 'image']
    success_url = reverse_lazy('blogs:home')
    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)