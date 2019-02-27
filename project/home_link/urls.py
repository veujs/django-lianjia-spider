from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [

    url(r'^$',views.house_index,name='house_index'),
    url(r'^spider/$',views.house_spider,name='house_spider'),
]