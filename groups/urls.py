from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('groups_list', views.GroupsList.as_view(), name='groups_list'),
    path('add/<int:pk>', views.add_to_group, name='add_to_group'),
    path('user_groups_list', views.UserGroupsList.as_view(), name='user_groups_list'),
    path('members_list/<int:pk>', views.members_list, name='members_list'),
    path('delete_group/<int:pk>', views.delete_group, name='delete_view'),
    path('edit_group/<int:pk>', views.EditGroup.as_view(), name='edit_group'),
    path('search/user/', views.search_user, name='search_user'),
    path('add_member/<int:group_id>', views.add_user_to_group, name='add_user_to_group'),
    path('search/member/<int:pk>/', views.search_member, name='search_member'),
    path('remove_member/<int:pk>', views.remove_member_from_group, name='remove_member'),
    path('create_group', views.CreateGroup.as_view(), name='create_group')
]