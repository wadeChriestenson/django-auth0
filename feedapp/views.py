from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post


# Create your views here.


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
        posts = Post.objects.filter(hidden=False).order_by('-date_posted').all()

        context = {'form': form, 'posts': posts}
    return render(request, 'feedapp/index.html', context)


def reports(request):
    return render(request, 'feedapp/reports.html')


# def delete_post(request, post_id):
#     # check if post belongs to user
#     post = Post.objects.get(id=post_id)
#     if post.user == request.user:
#         post.delete()
#     # remove it from the database
#     # redirect back to same page
#     return redirect('index')


@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://127.0.0.1:8000'  # this can be current domain
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')
