# -*- coding: utf-8 -*-

from django.conf.urls import url
from books.views import PublisherList

urlpatterns = [
    url(r'^publishers/$',PublisherList.as_view()),
]