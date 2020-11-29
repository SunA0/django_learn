from django.urls import path
from myproject.apps.board import views

urlpatterns = [
    path('boards/', views.boards, name='all_boards'),
    # topic
    path('board/<int:pk>/topics', views.topics, name='all_topics'),
    path('board/<int:pk>/topics/new', views.new_topic, name='new_topic'),

]
