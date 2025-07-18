from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from decouple import config
from .models import Post
from .forms import PostForm
#Flaw 5: Cross-Site Request Forgery (CSRF)
@csrf_exempt
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

#Flaw 3: A04:2021 – Insecure Design
def secret_api(request):
    key = request.GET.get('apikey')
    if key == 'my-secret-api-key':
        return JsonResponse({'data': 'Secrets!'})
    else:
        return JsonResponse({'error': 'Incorrect API key'}, status=403)

#Fix for Flaw 3: A04:2021-Insecure Design
#API_KEY = config('API_KEY')

#def secret_api(request):
    #key = request.GET.get('apikey')

    #if key == API_KEY:
        #return JsonResponse({'data': 'Secrets!'})
    #else:
        #return JsonResponse({'error': 'Incorrect API key'}, status=403)


