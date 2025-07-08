from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
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

def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'blog/profile.html', {'profile_user': user})

#@login_required
#def profile_view(request, user_id):
    #if request.user.id != user_id:
        #return HttpResponseForbidden("You do not have permission to view this profile.")
    #user = get_object_or_404(User, id=user_id)
    #return render(request, 'blog/profile.html', {'profile_user': user})