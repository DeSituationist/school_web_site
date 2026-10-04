from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    TrigramWordSimilarity,
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag

from .models import VKPost

def post_list(request, tag_slug=None):
    posts = VKPost.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__slug=tag_slug).distinct()

    all_tags = Tag.objects.all()

    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/post_list.html', {'page_obj': page_obj, 'tag': tag, 'all_tags': all_tags})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        VKPost,
        slug=slug,
        created__year=year,
        created__month=month,
        created__day=day,
    )

    return render(request, 'news/post_detail.html', {'post': post})

TYPO_SIMILARITY = 0.45

def post_search(request):
    query = request.GET.get('query', '').strip()[:100]
    posts = VKPost.objects.none()

    if len(query) >= 2:
        search_query = SearchQuery(query, config='russian', search_type='websearch')
        posts = (
            VKPost.objects
            .annotate(
                search=SearchVector('text', config='russian'),
                similarity=TrigramWordSimilarity(query, 'text'),
            )
            .filter(Q(search=search_query) | Q(similarity__gte=TYPO_SIMILARITY))
            .order_by('-similarity', '-created')
            .prefetch_related('tags')
        )

    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'news/post_search.html', {
        'page_obj': page_obj,
        'query': query,
        'total': paginator.count,
    })