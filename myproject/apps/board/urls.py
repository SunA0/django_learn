from django.urls import path
from myproject.apps.board import views

urlpatterns = [
    # path('boards/', views.boards, name='all_boards'),
    path('boards/', views.BoardsView.as_view(), name='all_boards'),
    # topic
    path('board/<int:pk>/topics', views.topics, name='all_topics'),
    path('board/<int:pk>/topics/new', views.new_topic, name='new_topic'),
    # post
    path('board/<int:pk>/topic/<int:topic_pk>/posts', views.posts, name='all_posts'),
    path('board/<int:pk>/topic/<int:topic_pk>/posts/new', views.new_post, name='new_post'),
    # path('board/<int:pk>/topic/<int:topic_pk>/posts/edit',views.PostUpdateView.as_view())
    #     url(r'^board/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
    #         boards_views.PostUpdateView.as_view(), name='edit_post'),

]
