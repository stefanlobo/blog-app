from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm

# Create your views here.


class PostListView(ListView):
    """
    Alternate post list view
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request):
    post_list = Post.published.all()

    # pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page not an int, get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):

    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    return render(
        request,
        "blog/post/detail.html",
        {"post": post},
    )


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        form = EmailPostForm()
    return render(
        request,
        "blog/post/share.html",
        {
            'post': post,
            'form': form
        }
    )
