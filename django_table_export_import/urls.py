# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns = [   
    url(r'^$', views.exports_list, name="table_export_list"),
    url(r'^import_file$', views.import_file, name="table_import_file"),
    url(r'^export_table/(?P<app_label>\w+)/(?P<model_id>\w+).(?P<extension>\w+)$', views.export_table, name="table_export"),
]


