from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /data/catalog/5/
    url(r'^catalog/(?P<catalog_id>[0-9]+)/$', views.catalog, name='catalog'),
    url(r'^catalog/(?P<catalog_id>[0-9]+)/node/(?P<node_id>[0-9]+)/$', views.node, name='node')
]