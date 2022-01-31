from django.contrib.auth import views
from django.urls import path
from .views import PostList, PostCreate, PostUpdate, PostDelete, Profile


app_name = 'account'
urlpatterns = [
    path('', PostList.as_view(), name="home"),
    path('post/create', PostCreate.as_view(), name="post-create"),
    path('post/update/<int:pk>', PostUpdate.as_view(), name="post-update"),
    path('post/delete/<int:pk>', PostDelete.as_view(), name="post-delete"),
    path('profile/', Profile.as_view(), name="profile"),
]