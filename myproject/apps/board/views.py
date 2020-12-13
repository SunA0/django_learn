from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def boards(request):
    board_boards = Board.objects.all()
    return render(request, 'boards/index.html', {'boards': board_boards})


# topic
def topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)
    try:
        all_topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        all_topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        all_topics = paginator.page(paginator.num_pages)

    return render(request, 'topics/index.html', {'board': board, 'topics': all_topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            user = request.user
            topic.board = board
            topic.starter = user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('all_topics', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'topics/new.html', {'form': form, 'board': board})


# posts
def posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'posts/index.html', {'topic': topic})


# FBV
@login_required
def new_post(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('all_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'posts/new.html', {'topic': topic, 'form': form})


# homepage
def about(request):
    # do something
    return render(request, 'about.html')


def about_company(request):
    # do something
    return render(request, 'about_company.html', {'company_name': 'Simple Complex'})

#
#
# class PostUpdateView(UpdateView):
#     model = Post
#     fields = ('message',)
#     template_name = 'posts/edit.html'
#     pk_url_kwarg = 'post_pk'
#     context_object_name = 'post'
#
#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.updated_by = self.request.user
#         post.updated_at = timezone.now()
#         post.save()
#         return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
#
# # FBV分页
#
#
# GCBV分页
