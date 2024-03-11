from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail



def post_list(request):
    post_list = Post.published.all()
    # Pagination with 5 post per page
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # if page number is out of range deliver last page of result
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if page number not an integer deliver first page
        posts = paginator.page(1)

    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {'post':post})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'thooriq.na@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html',
                  {'post':post, 'form':form, 'sent':sent})


