from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from django.shortcuts import render_to_response
import markdown


def index(request):
    projects = Post.objects.filter().order_by('-published_date')
    return render(request, 'base_index.html', {'projects': projects})


def blog(request, pk):
    blog = get_object_or_404(Post, pk=pk)
    if blog.text[0] != '$':
        blog.text = markdown.markdown(blog.text)
    else:
        blog.text = blog.text[1:]
    return render(request, 'base_blog.html', {'blog': blog})


def page_not_found(request):
    return render_to_response('404.html')


def hole(request):
    return render(request, 'hole.html')


def heat_plot(request):
    return render(request, 'heat_plot.json')


def week_heat(request):
    return render(request, 'week_heat.json')
