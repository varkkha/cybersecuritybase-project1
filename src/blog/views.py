from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db import connection
from .models import Post
from .forms import PostForm

@login_required
def index(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    else:
        form = PostForm()

    return render(request, 'blog/index.html', {'posts': posts, 'form': form})

#Flaw 1: A01:2021-Broken Access Control
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'blog/profile.html', {'profile_user': user})

#Fix for Flaw 1: A01:2021-Broken Access Control
#@login_required
#def profile_view(request, user_id):
    #if request.user.id != user_id:
        #return HttpResponseForbidden("You do not have permission to view this profile.")
    #user = get_object_or_404(User, id=user_id)
    #return render(request, 'blog/profile.html', {'profile_user': user})

#Flaw 2: A03:2021-Injection
def unsafe_search(request):
    name = request.GET.get('name')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM auth_user WHERE username = '{name}'")
        results = cursor.fetchall()
    return render(request, 'blog/results.html', {'results': results})

#Fix for Flaw 2: A03:2021-Injection
#def safe_search(request):
    #name = request.GET.get('name')
    #with connection.cursor() as cursor:
        #cursor.execute("SELECT * FROM auth_user WHERE username = %s", [name])
        #results = cursor.fetchall()
    #return render(request, 'blog/results.html', {'results': results})