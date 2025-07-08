# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
]