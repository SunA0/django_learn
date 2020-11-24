from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post
from django.views.generic import UpdateView, ListView
from django.utils import timezone

from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# CBV
# class NewPostView(View):
#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#         return render(request, 'new_post.html', {'form': form})
#
#     def get(self, request):
#         form = PostForm()
#         return render(request, 'new_post.html', {'form': form})


# GCBV
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
#
#
# class NewPostView(CreateView):
#     model = Post
#     form_class = PostForm
#     success_url = reverse_lazy('post_list')
#     template_name = 'new_post.html'


def home(request):
    boards = Board.objects.all()
    return render(request, 'boards/index.html', {'boards': boards})


def about(request):
    # do something
    return render(request, 'about.html')


def about_company(request):
    # do something
    return render(request, 'about_company.html', {'company_name': 'Simple Complex'})


def topics(request, pk):
    # board = Board.objects.get(pk=pk)
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics/index.html', {'board': board, 'topics': topics})


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
            return redirect('topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'topics/new.html', {'form': form, 'board': board})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'posts/index.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'posts/new.html', {'topic': topic, 'form': form})


class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'posts/edit.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

# FBV分页


# GCBV分页
