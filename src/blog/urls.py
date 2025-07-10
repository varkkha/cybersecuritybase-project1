# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('unsafe-search/', views.unsafe_search, name='unsafe_search'),
    #path('safe-search/', views.safe_search, name='safe_search'),
    path('secret-api/', views.secret_api, name='secret_api'),
]