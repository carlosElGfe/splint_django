# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('new_splint',views.new_splint,name="new_splint"),
    path('visualize/<str:code>', views.visualize,name="visualize"),
    path('search_splint', views.visualize,name="search_splint"),
    path('download_splint_stl/<str:code>',views.down_stl,name="download_splint_stl"),
    path('database',views.data_base,name="database"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
