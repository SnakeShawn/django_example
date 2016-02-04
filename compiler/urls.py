from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compile/$', views.compile, name='compile'),
    url(r'^invoke/$', views.invoke, name='invoke'),
    url(r'^result/$', views.result, name='result'),
]
