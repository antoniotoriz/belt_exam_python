from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^job$', views.job),
    url(r'^add_job$', views.add_job),
    url(r'^jobs/(?P<id>\d+)$', views.jobs_id),
    url(r'^jobs/edit/(?P<id>\d+)$', views.edit),
    url(r'^edit_job/(?P<id>\d+)$', views.edit_job),
    url(r'^delete_job/(?P<id>\d+)$', views.delete_job),
    url(r'^add_favorites/(?P<id>\d+)$', views.add_favorites),
    url(r'^remove_favorites/(?P<id>\d+)$', views.remove_favorites),
    url(r'^logout$', views.logout),
]
