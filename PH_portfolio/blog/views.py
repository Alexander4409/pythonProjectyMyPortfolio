from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Blog
from .forms import BlogForm


def blogs(request):
    blogi = Blog.objects.order_by("-date")
    return render(request, 'blog/blogs.html', {'blogs': blogi})


def details(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/details.html', {'blog': blog})


@user_passes_test(lambda u: u.is_staff)
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blogs')
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})


@user_passes_test(lambda u: u.is_staff)
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/edit_blog.html', {'form': form, 'blog': blog})
