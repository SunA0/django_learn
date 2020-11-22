from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewTopicForm
from .models import Board, Topic, Post


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
    return render(request, 'topics/index.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            user = User.objects.first()
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
