from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('sign_up', views.SignUpView.as_view(), name='sign_up'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('edit_profile/', views.UserEditView.as_view(), name='edit'),
    path('delete_image/<int:pk>', views.delete_image, name='delete_image')
]