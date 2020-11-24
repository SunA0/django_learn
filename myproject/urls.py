from django.conf.urls import url
from django.contrib import admin

from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from boards import views as boards_views

# todo url()=> path()
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # root
    url(r'^$', boards_views.home, name='home'),

    # topics
    url(r'^boards/(?P<pk>\d+)/$', boards_views.topics, name='topics'),
    # about
    url(r'^about/$', boards_views.about, name='about'),
    # about company
    url(r'^about/company/$', boards_views.about_company, name='about_company'),
    # topics new
    url(r'^boards/(?P<pk>\d+)/new/$', boards_views.new_topic, name='new_topic'),
    # topic post
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', boards_views.topic_posts, name='topic_posts'),
    # post new
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', boards_views.reply_topic, name='reply_topic'),
    # post edit
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        boards_views.PostUpdateView.as_view(), name='edit_post'),
    # accounts
    # signup
    url(r'^signup/$', accounts_views.signup, name='signup'),
    # logout
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    # login
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # reset
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),
    # edit password
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),

]
