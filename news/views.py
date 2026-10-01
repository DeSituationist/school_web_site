from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator
from .models import VKPost

# Create your views here.
def post_list(request, tag_slug=None):
    posts = VKPost.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__slug=tag_slug).distinct()

    all_tags = Tag.objects.all()

    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/post_list.html', {'page_obj': page_obj, 'tag': tag, 'all_tags': all_tags})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        VKPost, 
        slug=slug,
        created__year = year,
        created__month = month,
        created__day = day,
    )

    return render(request, 'news/post_detail.html', {'post': post})