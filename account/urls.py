# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth.views import login,logout,logout_then_login,password_change
from django.contrib.auth.views import password_change_done ,password_reset,password_reset_done,password_reset_confirm,password_reset_complete

urlpatterns = [
    #url(r'^login/$',views.user_login,name='login'),
    # login / logout urls  
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', login, name='login'),
    #url(r'^logout/$',django.contrib.auth.views.logout,name='logout'),
    #url(r'logged_out/$',views.user_logout,name='logged_out'),  
    url(r'^logged_out/$',logout, {'template_name': 'account/logged_out.html'},name='logged_out'),    
    url(r'^logout-then-login/$',logout_then_login,name='logout_then_login'),

    #change password urls
    #url(r'^password-change/$', password_change, {'template_name': 'registration/password_change_form.html'},name='password_change'),
    url(r'^password-change/$',password_change, {'template_name': 'account/password_change_form.html'},name='password_change') ,   
    url(r'^password-change/done/$',password_change_done,{'template_name': 'account/password_change_done.html'},name='password_change_done'),

    # restore password urls
    url(r'^password-reset/$',password_reset,{'template_name':'account/password_reset_form.html'},name='password_reset'),
    url(r'^password-reset/done/$',password_reset_done,{'template_name':'account/password_reset_done.html'},name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',password_reset_confirm,{'template_name':'account/password_reset_confirm.html'},name='password_reset_confirm'),
    url(r'^password-reset/complete/$',password_reset_complete,{'template_name':'account/password_reset_complete.html'},name='password_reset_complete'),
    url(r'^register/$',views.register,name='register'),
    url(r'^edit/$',views.edit,name='edit'),
]






