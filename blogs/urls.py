from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('posts/<int:pk>', views.UserBlog.as_view(), name='user_blog'),
    path('create_post', views.CreatePost.as_view(), name='create_post'),
    path('post_detail/<int:pk>/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('edit_post/<int:pk>', views.EditPost.as_view(), name='edit_post'),
    path('delete_post/<int:pk>', views.DeletePost.as_view(), name='delete_post')

]